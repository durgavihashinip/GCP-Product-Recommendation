import streamlit as st
import requests
import json
import subprocess

def call_api(user_id: int, item_name: str):
    """Calls the recommendation API with the given user ID and item name."""
    api_url = "https://get-product-recommendation-874367124365.us-central1.run.app"
    headers = {
        "Authorization": f"bearer {get_auth_token()}",
        "Content-Type": "application/json",
    }
    data = {"user_id": user_id, "item_name": item_name}
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

def get_auth_token():
    """Gets the Google Cloud identity token."""
    try:
        command = ["gcloud", "auth", "print-identity-token"]
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error getting auth token: {e}"
    except FileNotFoundError:
        return "Error: gcloud command not found. Please ensure Google Cloud CLI is installed and configured."

def display_recommendations_horizontal(recommendations):
    """Displays recommendations horizontally with details in a dropdown."""
    if "error" in recommendations:
        st.error(recommendations["error"])
        return

    if not recommendations:
        st.info("No recommendations found.")
        return

    st.subheader("Recommended Products:")
    for product in recommendations:
        with st.expander(product.get('Name', 'N/A')):
            st.write(f"- **Brand:** {product.get('Brand', 'N/A')}")
            st.write(f"- **Rating:** {product.get('Rating', 'N/A')}")
            review_count = product.get('ReviewCount', 'N/A')
            st.write(f"- **Review Count:** {review_count}")
            product_price = product.get('Product Price', 'N/A')
            st.write(f"- **Product Price (USD):** ${product_price:.2f}" if isinstance(product_price, (int, float)) else f"- **Product Price (USD):** {product_price}")
            price_in_inr = product.get('Price_In_INR', 'N/A')
            st.write(f"- **Price (INR):** ₹{price_in_inr:.2f}" if isinstance(price_in_inr, (int, float)) else f"- **Price (INR):** {price_in_inr}")
            image_urls = product.get('ImageURL', '').split(' | ')
            for url in image_urls:
                st.image(url, caption=product.get('Name', 'Product Image'), width=200)
            st.markdown("---")

def main():
    st.title("RELANTO Recommendation System")

    user_id = st.number_input("Enter User ID:", min_value=0, step=1)
    item_name = st.text_input("Enter Item Name:")

    if st.button("Get Recommendations"):
        if item_name:
            with st.spinner("Fetching recommendations..."):
                recommendations = call_api(user_id, item_name)
            display_recommendations_horizontal(recommendations)
        else:
            st.warning("Please enter an item name.")

if __name__ == "__main__":
    main()