import pytest
import pandas as pd
import json
from main import clean_and_extract_tags, content_based_recommendations
 
# Load real sample data
with open('test_data/sample_products.json') as f:
    REAL_SAMPLE_DATA = pd.DataFrame(json.load(f))
 
def test_with_real_data():
    """Test with actual data samples from your dataset"""
    # Test cleaning real product descriptions using the hair color product since it has a description
    result = clean_and_extract_tags(REAL_SAMPLE_DATA.iloc[1]['Product Description'])
    assert "natural" in result
    assert "color" in result
    assert "permanent" in result
 
    # Test recommendations with real products
    recs = content_based_recommendations(
        REAL_SAMPLE_DATA, 
        'OPI Infinite Shine, Nail Lacquer Nail Polish, Bubble Bath',
        top_n=1
    )
    assert len(recs) == 1
    # Since there are only two products, the recommendation should be the hair color product
    assert recs.iloc[0]['Product Name'] == 'Nice n Easy Permanent Color, 111 Natural Medium Auburn 1 ea (Pack of 3)'