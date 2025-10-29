# 🛍️ Fashion Studio ETL Pipeline

A complete ETL pipeline for scraping fashion product data with data cleaning and multiple storage options.

## 🚀 Features
- Web scraping 1000+ products from 50 pages
- Data transformation and cleaning
- Multiple storage (CSV, PostgreSQL, Google Sheets)
- Unit testing with 69% coverage

## 🛠️ Tech Stack
- Python, Pandas, BeautifulSoup
- PostgreSQL, Google Sheets API
- Pytest, Coverage

## 📊 Results
- **Input**: 1000 raw records
- **Output**: 867 clean records  
- **Success Rate**: 86.7%
- **Test Coverage**: 69%

## 🎯 Quick Start
```bash
# Run ETL pipeline
python main.py

# Run tests
python -m pytest test/ -v

# Check coverage
coverage run -m pytest test/
coverage report