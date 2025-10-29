#transform.py
import pandas as pd
import re
from datetime import datetime

EXCHANGE_RATE = 16000  

class TransformError(Exception):
    pass

def _parse_price(price_str):
    if not price_str or "Unavailable" in price_str or "Price Unavailable" in price_str:
        return None
    
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", price_str)
    if not m:
        return None
    
    usd = float(m.group(1).replace(",", ""))
    idr = int(round(usd * EXCHANGE_RATE))
    return idr

def _parse_rating(rating_str):
    if not rating_str:
        return 0.0
    
    rating_str = str(rating_str)
    
    if "Invalid Rating" in rating_str:
        return None  
    
    if "No Rating" in rating_str:
        return 0.0
    
    m = re.search(r"(\d+\.\d+)\s*/\s*5", rating_str)
    if m:
        return float(m.group(1))
    
    m = re.search(r"(\d+(?:\.\d+)?)", rating_str)
    if m:
        rating_value = float(m.group(1))
        if 0 <= rating_value <= 5:
            return rating_value
    return 0.0

def _parse_colors(colors_str):
    if not colors_str:
        return 1
    m = re.search(r"(\d+)", colors_str)
    return int(m.group(1)) if m else 1

def _clean_size(size_str):
    if not size_str:
        return "M"
    return size_str.replace("Size:", "").strip()

def _clean_gender(gender_str):
    if not gender_str:
        return "Unisex"
    return gender_str.replace("Gender:", "").strip()

def transform_records(records):
    if not records:
        raise TransformError("No records to transform.")
    
    df = pd.DataFrame(records)
    print(f"Raw data count: {len(df)}")
    print(f"Raw data sample (first 3):")
    print(f"  Title: {df['title'].head(3).tolist()}")
    print(f"  Price: {df['price'].head(3).tolist()}")
    print(f"  Rating: {df['rating'].head(3).tolist()}")
    
    df["price_idr"] = df["price"].apply(_parse_price)
    df["rating_parsed"] = df["rating"].apply(_parse_rating)
    df["colors_count"] = df["colors"].apply(_parse_colors)
    df["size_clean"] = df["size"].apply(_clean_size)
    df["gender_clean"] = df["gender"].apply(_clean_gender)

    out = pd.DataFrame({
        "title": df["title"],
        "price": df["price_idr"],
        "rating": df["rating_parsed"],
        "colors": df["colors_count"],
        "size": df["size_clean"],
        "gender": df["gender_clean"],
        "timestamp": df["timestamp"]
    })

    print(f"\n=== FILTERING DATA ===")
    print(f"Before filter: {len(out)} records")
    
    unknown_product_count = (out["title"] == "Unknown Product").sum()
    price_unavailable_count = out["price"].isnull().sum()
    invalid_rating_count = out["rating"].isnull().sum()
    
    print(f"  - Unknown Product: {unknown_product_count}")
    print(f"  - Price Unavailable: {price_unavailable_count}")
    print(f"  - Invalid Rating: {invalid_rating_count}")

    out = out[
        (out["title"] != "Unknown Product") &
        (out["price"].notnull()) &
        (out["rating"].notnull())
    ].copy()
    
    print(f"After filter: {len(out)} records")

    out["rating"] = out["rating"].fillna(0.0)
    out["colors"] = out["colors"].fillna(1)
    out["size"] = out["size"].fillna("M")
    out["gender"] = out["gender"].fillna("Unisex")

    out["price"] = out["price"].astype('float64')
    out["rating"] = out["rating"].astype('float64')
    out["colors"] = out["colors"].astype('int64')
    out["size"] = out["size"].astype(str)
    out["gender"] = out["gender"].astype(str)
    out["timestamp"] = pd.to_datetime(out["timestamp"])

    before_dedup = len(out)
    out = out.drop_duplicates() 
    duplicates_removed = before_dedup - len(out)
    print(f"Duplicates removed: {duplicates_removed}")
    
    out = out.reset_index(drop=True)

    print(f"\n=== FINAL STATS ===")
    print(f"Total records: {len(out)}")
    print(f"Rating distribution:")
    print(f"  - 0.0 (No Rating): {(out['rating'] == 0.0).sum()}")
    print(f"  - 1.0-2.0: {((out['rating'] >= 1.0) & (out['rating'] < 2.0)).sum()}")
    print(f"  - 2.0-3.0: {((out['rating'] >= 2.0) & (out['rating'] < 3.0)).sum()}")
    print(f"  - 3.0-4.0: {((out['rating'] >= 3.0) & (out['rating'] < 4.0)).sum()}")
    print(f"  - 4.0-5.0: {((out['rating'] >= 4.0) & (out['rating'] <= 5.0)).sum()}")
    print(f"\nSample records after transform:")
    print(out.head(3).to_string())

    if out.empty:
        raise TransformError("No valid records after transformation.")
    
    return out