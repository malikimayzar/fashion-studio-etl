import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.transform import transform_records, _parse_price, _parse_rating, _parse_colors, _clean_size, _clean_gender
import pandas as pd

def test_transform_data():
    sample_data = [{
        "title": "Test Product",
        "price": "$100.00", 
        "rating": "Rating:  4.5 / 5",
        "colors": "3 Colors",
        "size": "Size: M",
        "gender": "Gender: Men",
        "timestamp": "2025-01-01T00:00:00"
    }]
    
    result = transform_records(sample_data)
    assert len(result) == 1
    assert result.iloc[0]["price"] == 1600000  
    assert result.iloc[0]["rating"] == 4.5
    assert result.iloc[0]["colors"] == 3
    assert result.iloc[0]["size"] == "M"
    assert result.iloc[0]["gender"] == "Men"
    print("test_transform_data PASSED!")

def test_transform_invalid_data():
    sample_data = [
        {
            "title": "Unknown Product", 
            "price": "$100.00",
            "rating": "Rating:  4.5 / 5", 
            "colors": "3 Colors",
            "size": "Size: M",
            "gender": "Gender: Men",
            "timestamp": "2025-01-01T00:00:00"
        },
        {
            "title": "Valid Product",
            "price": "$50.00",
            "rating": "Rating:  3.8 / 5",
            "colors": "2 Colors", 
            "size": "Size: L",
            "gender": "Gender: Women",
            "timestamp": "2025-01-01T00:00:00"
        }
    ]
    
    result = transform_records(sample_data)
    assert len(result) == 1 
    assert result.iloc[0]["title"] == "Valid Product"
    print("test_transform_invalid_data PASSED!")

def test_parse_price():
    assert _parse_price("$100.00") == 1600000 
    assert _parse_price("$50.50") == 808000     
    assert _parse_price("Price Unavailable") is None
    assert _parse_price("") is None
    print("test_parse_price PASSED!")

def test_parse_rating():
    assert _parse_rating("Rating: 4.5/5") == 4.5
    assert _parse_rating("4.8/5") == 4.8
    assert _parse_rating("No Rating") == 0.0
    assert _parse_rating("Invalid Rating") is None
    print("test_parse_rating PASSED!")

def test_parse_colors():
    assert _parse_colors("3 Colors") == 3
    assert _parse_colors("1 Color") == 1
    assert _parse_colors("No Colors") == 1  
    print("test_parse_colors PASSED!")

def test_clean_size():
    assert _clean_size("Size: M") == "M"
    assert _clean_size("Size:L") == "L" 
    assert _clean_size("") == "M"  
    print("test_clean_size PASSED!")

def test_clean_gender():
    assert _clean_gender("Gender: Men") == "Men"
    assert _clean_gender("Gender:Women") == "Women"
    assert _clean_gender("") == "Unisex"  
    print("test_clean_gender PASSED!")

if __name__ == "__main__":
    test_transform_data()
    test_transform_invalid_data()
    test_parse_price()
    test_parse_rating() 
    test_parse_colors()
    test_clean_size()
    test_clean_gender()