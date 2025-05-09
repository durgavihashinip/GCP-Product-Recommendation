from main import clean_and_extract_tags, content_based_recommendations
import pandas as pd

def test_clean_and_extract_tags():
    text = "This is a sample product description!"
    result = clean_and_extract_tags(text)
    assert isinstance(result, str)
    assert "sample" in result

def test_content_based_recommendations():
    df = pd.DataFrame({
        'Name': ['Clairol Nice N Easy Permanent Color 7/106A Natural Dark Neutral Blonde, 1.0 KIT', 'Old Spice Artisan Styling High Hold Matte Finish Molding Clay, 2.64 oz', 'Old Spice Artisan Styling High Hold Matte Finish Molding Clay, 2.64 oz'],
        'Tags': ['Clairol Nice \'N Easy Permanent Color 7/106A Natural Dark Neutral Blonde, 1.0 KIT, Wal-mart, Walmart.com', 'Old Spice Artisan Styling High Hold Matte Finish Molding Clay, 2.64 oz, Wal-mart, Walmart.com', 'Colgate My First Baby and Toddler Toothpaste, Fluoride Free and SLS Free, 1.75 Oz, Wal-mart, Walmart.com'],
        'ReviewCount': [29221, 52, 10],
        'Brand': ['Clairol','Old Spice','Colgate'],
        'ImageURL': ['https://www.walmart.com/ip/Clairol-Nice-N-Easy-Permanent-Color-7-106A-Natural-Dark-Neutral-Blonde-1-0-KIT/10316864?selected=true','https://www.walmart.com/ip/Old-Spice-Mens-Styling-Molding-Clay-High-Hold-Matte-Finish-2-64-oz/34201687?selected=true', 'https://www.walmart.com/ip/Colgate-My-First-Baby-and-Toddler-Toothpaste-Fluoride-Free-and-SLS-Free-1-75-Oz/36073552?selected=true'],
        'Rating': [4.5,4.6,4.3],
        'Product Price': [7.99, 6.97, 2.94],
        'Price_In_INR': [677.312, 590.8469, 249.22379999999998]
    })
    recs = content_based_recommendations(df, 'Clairol Nice N Easy Permanent Color 7/106A Natural Dark Neutral Blonde, 1.0 KIT')
    assert not recs.empty
