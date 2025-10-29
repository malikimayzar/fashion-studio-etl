import argparse
from utils.extract import scrape_all
from utils.transform import transform_records
from utils.load import save_csv, save_google_sheets, save_postgres
import os

def parse_args():
    parser = argparse.ArgumentParser(description='ETL Pipeline for Fashion Products')
    parser.add_argument('--pages', type=int, default=50, help='Number of pages to scrape')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between requests')
    parser.add_argument('--output', type=str, default='products.csv', help='Output CSV path')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    return parser.parse_args()

def run():
    print("Start scraping...")
    raw = scrape_all(pages=50, delay=0.5)  
    print(f"Scraped {len(raw)} raw items")
    print(raw[:3])


    print("Transforming...")
    df = transform_records(raw)
    print(f"{len(df)} records after transform")

    print("Saving CSV...")
    csv_path = save_csv(df, path="products.csv")
    print("Saved CSV:", csv_path)

    gs_json = os.getenv("GOOGLE_SHEETS_JSON")  
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if gs_json:
        try:
            url = save_google_sheets(df, service_json_path=gs_json, sheet_id=sheet_id)
            print("Saved Google Sheet:", url)
        except Exception as e:
            print("Google Sheets save failed:", e)

    db_url = os.getenv("DATABASE_URL")
    if db_url:
        try:
            save_postgres(df, db_url)
            print("Saved to Postgres")
        except Exception as e:
            print("Postgres save failed:", e)

if __name__ == "__main__":
    run()
