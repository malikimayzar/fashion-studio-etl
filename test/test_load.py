# test/test_load.py
import pandas as pd
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# ✅ PERBAIKAN: Import dari utils.load, bukan src.load
from utils.load import save_csv, save_postgres, save_google_sheets

def test_save_csv():
    df = pd.DataFrame([{
        "title": "Test Product",
        "price": 1600000,
        "rating": 4.5,
        "colors": 3,
        "size": "L",
        "gender": "Unisex",
        "timestamp": "2025-01-01T00:00:00"
    }])
    
    test_path = "test_output.csv"
    path = save_csv(df, path=test_path)
  
    assert os.path.exists(path)
    
    loaded_df = pd.read_csv(path)
    assert len(loaded_df) == 1
    assert loaded_df.iloc[0]["title"] == "Test Product"
    assert loaded_df.iloc[0]["price"] == 1600000
    
    os.remove(test_path)
    print("test_save_csv PASSED!")

# ✅ PERBAIKAN: Ganti patch path ke utils.load
@patch('utils.load.create_engine')
def test_save_postgres(mock_create_engine):
    """Test save_postgres function"""
    # Mock database engine
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    
    mock_engine.connect.return_value.__enter__ = MagicMock(return_value=mock_connection)
    mock_engine.connect.return_value.__exit__ = MagicMock(return_value=None)
    mock_create_engine.return_value = mock_engine
    
    # Test data
    df = pd.DataFrame({
        'title': ['Test Product'],
        'price': [1600000],
        'rating': [4.5]
    })
    
    # Test function - ✅ save_postgres sekarang terdefinisi
    result = save_postgres(df, 'postgresql://test:test@localhost/test', 'products')
    
    assert result is True
    print("test_save_postgres PASSED!")

# ✅ PERBAIKAN: Ganti patch path ke utils.load
@patch('utils.load.gspread.authorize')
@patch('utils.load.Credentials.from_service_account_file')
def test_save_google_sheets(mock_creds, mock_auth):
    """Test save_google_sheets function"""
    # Mock Google Sheets objects
    mock_credential = MagicMock()
    mock_creds.return_value = mock_credential
    
    mock_client = MagicMock()
    mock_auth.return_value = mock_client
    
    mock_worksheet = MagicMock()
    mock_client.open_by_key.return_value = mock_worksheet
    mock_worksheet.worksheet.return_value = mock_worksheet
    mock_worksheet.url = "https://docs.google.com/test"
    
    # Test data
    df = pd.DataFrame({
        'title': ['Test Product'],
        'price': [1600000]
    })
    
    # Test function
    result = save_google_sheets(df, 'test_credentials.json', 'test_sheet_id', 'test_sheet')
    
    assert 'https://' in result
    print("test_save_google_sheets PASSED!")

if __name__ == "__main__":
    test_save_csv()
    test_save_postgres()
    test_save_google_sheets()