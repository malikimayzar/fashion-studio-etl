# test/test_extract.py
import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.extract import scrape_page, scrape_all, parse_product_card  # ✅ Gunakan utils
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

def test_parse_product_card_minimal():
    html = """
    <div class="collection-card">
      <h3 class="product-title">T-Shirt A</h3>
      <span class="price">$10.00</span>
      <p style="font-size: 14px; color: #777;">Rating:  4.5 / 5</p>
      <p style="font-size: 14px; color: #777;">3 Colors</p>
      <p style="font-size: 14px; color: #777;">Size: M</p>
      <p style="font-size: 14px; color: #777;">Gender: Men</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    card = soup.select_one(".collection-card")
    
    got = parse_product_card(card)
    
    assert got["title"] == "T-Shirt A"
    assert got["price"] == "$10.00"  
    assert "4.5" in got["rating"]
    assert got["colors"] == "3 Colors"
    assert got["size"] == "Size: M"
    assert got["gender"] == "Gender: Men"
    print("test_parse_product_card_minimal PASSED!")

def test_scrape_all_mock():
    with patch('utils.extract.requests.Session') as mock_session:
        mock_response = MagicMock()
        mock_response.text = """
        <html>
          <div class="collection-card">
            <h3>Test Product</h3>
            <span class="price">$15.00</span>
            <p>Rating:  4.0 / 5</p>
            <p>2 Colors</p>
            <p>Size: L</p>
            <p>Gender: Women</p>
          </div>
        </html>
        """
        mock_session.return_value.get.return_value = mock_response
        
        result = scrape_all(pages=1, delay=0)
        assert len(result) > 0
        print("test_scrape_all_mock PASSED!")

# ✅ PERBAIKAN: Hapus 'self' parameter
@patch('utils.extract.requests.Session')
def test_scrape_page_success(mock_session):  # ❌ HAPUS 'self'
    """Test scrape_page function specifically"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """
    <html>
      <div class="collection-card">
        <h3 class="product-title">Test Product Page</h3>
        <span class="price">$25.00</span>
        <p>Rating: 4.2/5</p>
        <p>4 Colors</p>
        <p>Size: XL</p>
        <p>Gender: Unisex</p>
      </div>
    </html>
    """
    
    mock_session_instance = MagicMock()
    mock_session_instance.get.return_value = mock_response
    mock_session.return_value = mock_session_instance
    
    # Test scrape_page directly
    result = scrape_page(1)
    
    assert len(result) == 1
    assert result[0]['title'] == 'Test Product Page'
    assert result[0]['price'] == '$25.00'
    print("test_scrape_page_success PASSED!")

if __name__ == "__main__":
    test_parse_product_card_minimal()
    test_scrape_all_mock() 
    test_scrape_page_success()