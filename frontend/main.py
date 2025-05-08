import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import json
import subprocess
import bigframes.pandas as bf

bf.options.bigquery.location = "us-central1"
bf.options.bigquery.project = "carbon-beanbag-452610-q6"

def clean_and_extract_tags(text):
    if isinstance(text, str):
        lower_text = text.lower()
        tokens = re.findall(r'\b\w+\b', lower_text)  # Tokenize using regex
        tags = [token for token in tokens if token.isalnum() and token not in STOP_WORDS]
        return ', '.join(tags)
    else:
        return ''

# def load_spacy_model():
#     """Downloads and loads the SpaCy model."""
#     try:
#         return spacy.load("en_core_web_sm")
#     except OSError:
#         print("Downloading en_core_web_sm model...")
#         subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
#         return spacy.load("en_core_web_sm")


# nlp = load_spacy_model()


# def clean_and_extract_tags(text):
#     if isinstance(text, str):
#         doc = nlp(text.lower())
#         tags = [token.text for token in doc if token.text.isalnum() and token.text not in STOP_WORDS]
#         return ', '.join(tags)
#     else:
#         return ''


def content_based_recommendations(train_data, item_name, top_n=10):
    if item_name not in train_data['Name'].values:
        return f"Item '{item_name}' not found in the training data."

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)
    item_index = train_data[train_data['Name'] == item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n + 1]
    recommended_item_indices = [x[0] for x in top_similar_items]
    recommended_items_details = train_data.iloc[recommended_item_indices][
        ['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating','Product Price','Price_In_INR']]
    return recommended_items_details


def collaborative_filtering_recommendations(train_data, target_user_id, top_n=10):
    user_item_matrix = train_data.pivot_table(index='ID', columns='ProdID', values='Rating', aggfunc='mean').fillna(0)
    user_similarity = cosine_similarity(user_item_matrix)
    if target_user_id not in user_item_matrix.index:
        return f"User ID {target_user_id} not found in the data."
    target_user_index = user_item_matrix.index.get_loc(target_user_id)
    user_similarities = user_similarity[target_user_index]
    similar_users_indices = user_similarities.argsort()[::-1][1:]
    recommended_items = []
    for user_index in similar_users_indices:
        rated_by_similar_user = user_item_matrix.iloc[user_index]
        not_rated_by_target_user = (rated_by_similar_user == 0) & (user_item_matrix.iloc[target_user_index] == 0)
        recommended_items.extend(user_item_matrix.columns[not_rated_by_target_user][:top_n])
    recommended_items_details = train_data[train_data['ProdID'].isin(recommended_items)][
        ['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating','Product Price','Price_In_INR']]
    return recommended_items_details.head(top_n)


def hybrid_recommendations(train_data, target_user_id, item_name, top_n=10):
    content_based_rec = content_based_recommendations(train_data, item_name, top_n)
    collaborative_filtering_rec = collaborative_filtering_recommendations(train_data, target_user_id, top_n)
    hybrid_rec = pd.concat([content_based_rec, collaborative_filtering_rec]).drop_duplicates()
    return hybrid_rec.head(top_n)


def main(request):
    """Responds to an HTTP request.

    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using `flask.make_response`.
    """
    request_json = request.get_json(silent=True)
    target_user_id = request_json.get('user_id')
    item_name = request_json.get('item_name')

    if not target_user_id or not item_name:
        return json.dumps({"error": "Please provide 'user_id' and 'item_name' in the request."}), 400, {
            'ContentType': 'application/json'}

    try:
        bf.options.bigquery.location = "us-central1"
        bf.options.bigquery.project = "carbon-beanbag-452610-q6"
        bf_data = bf.read_gbq("carbon-beanbag-452610-q6.recommendationDataset.transformed_data")
        train_data = bf_data.to_pandas()
        train_data = train_data[
            ['Uniq Id', 'Product Id', 'Product Rating', 'Product Reviews Count', 'Product Category', 'Product Brand',
             'Product Name', 'Product Image Url', 'Product Description', 'Product Tags','Product Price','Price_In_INR']]

        column_name_mapping = {
            'Uniq Id': 'ID',
            'Product Id': 'ProdID',
            'Product Rating': 'Rating',
            'Product Reviews Count': 'ReviewCount',
            'Product Category': 'Category',
            'Product Brand': 'Brand',
            'Product Name': 'Name',
            'Product Image Url': 'ImageURL',
            'Product Description': 'Description',
            'Product Tags': 'Tags',
            'Product Contents': 'Contents',
            'Product Price':'Product Price',
            'Price_In_INR':'Price_In_INR'
        }
        train_data = train_data.rename(columns=column_name_mapping)
        train_data['ID'] = train_data['ID'].str.extract(r'(\d+)').astype(float)
        train_data['ProdID'] = train_data['ProdID'].str.extract(r'(\d+)').astype(float)
        columns_to_extract_tags_from = ['Category', 'Brand', 'Description']
        for column in columns_to_extract_tags_from:
            train_data[column] = train_data[column].apply(clean_and_extract_tags)
        train_data['Tags'] = train_data[columns_to_extract_tags_from].apply(lambda row: ', '.join(row), axis=1)

        hybrid_rec = hybrid_recommendations(train_data, target_user_id, item_name, top_n=10)
        hybrid_rec_json = hybrid_rec.to_json(orient='records')
        return hybrid_rec_json, 200, {'ContentType': 'application/json'}

    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'ContentType': 'application/json'}