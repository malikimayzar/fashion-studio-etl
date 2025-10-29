#load.py
import pandas as pd
import csv
from sqlalchemy import create_engine
import gspread
from google.oauth2.service_account import Credentials

class LoadError(Exception):
    pass

def save_csv(df: pd.DataFrame, path="products.csv"):
    try:
        df.to_csv(path, index=False)
        return path
    except Exception as e:
        raise LoadError(f"failed saving csv: {e}")

def save_google_sheets(df: pd.DataFrame, service_json_path, sheet_id=None, sheet_name="products"):
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(service_json_path, scopes=scopes)
        gc = gspread.authorize(creds)
        if sheet_id:
            sh = gc.open_by_key(sheet_id)
        else:
            sh = gc.create(sheet_name)
        try:
            worksheet = sh.worksheet(sheet_name)
        except Exception:
            worksheet = sh.add_worksheet(title=sheet_name, rows="1000", cols="20")
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        return sh.url
    except Exception as e:
        raise LoadError(f"failed saving to Google Sheets: {e}")

def save_postgres(df: pd.DataFrame, db_url, table_name="products"):
    try:
        engine = create_engine(db_url, echo=False, future=True)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        return True
    except Exception as e:
        raise LoadError(f"failed saving to Postgres: {e}")
