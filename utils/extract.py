#extract.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

BASE_URL = "https://fashion-studio.dicoding.dev/"

class ScrapeError(Exception):
    pass

def _get_soup(url, session=None, timeout=10, retries=3, backoff=1.0):
    session = session or requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ETL-Bot/1.0)"}
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            r = session.get(url, headers=headers, timeout=timeout)
            r.raise_for_status()
            return BeautifulSoup(r.text, "html.parser")
        except requests.RequestException as e:
            last_exc = e
            if attempt < retries:
                time.sleep(backoff * attempt)
                continue
            raise ScrapeError(f"request failed for {url}: {e}")
    raise ScrapeError(f"request failed for {url}: {last_exc}")

def _text_or_none(node):
    return node.get_text(strip=True) if node else None

def parse_product_card(card):
    title_node = card.select_one(".product-title") or card.select_one("h3") or card.select_one("h2")
    title = _text_or_none(title_node) or "Unknown Product"

    price_node = card.select_one(".price-container .price") or card.select_one(".price")
    price = _text_or_none(price_node) or "Price Unavailable"

    rating = "No Rating"
    rating_p = card.find("p", string=lambda t: t and "Rating:" in t and " " in t)
    if rating_p:
        rating = _text_or_none(rating_p)
    else:
        rating_node = card.find("p", string=lambda t: t and " " in t)
        if rating_node:
            rating = _text_or_none(rating_node)

    colors = "0 Colors"
    size = "Unknown Size"
    gender = "Unknown Gender"

    p_tags = card.select("p")

    for p in p_tags:
        txt = _text_or_none(p)
        if not txt:
            continue
        
        txt_lower = txt.lower()
        
        if "$" in txt or "rating:" in txt_lower or "/5" in txt:
            continue
        
        if "color" in txt_lower:
            colors = txt
        elif "size:" in txt_lower:
            size = txt
        elif "gender:" in txt_lower:
            gender = txt

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "colors": colors,
        "size": size,
        "gender": gender,
    }

def scrape_page(page_num, session=None):
    session = session or requests.Session()
    if page_num == 1:
        url = BASE_URL
    else:
        url = f"{BASE_URL}page{page_num}"
    soup = _get_soup(url, session=session)
    cards = soup.select(".collection-card")
    results = [parse_product_card(card) for card in cards]
    return results

def scrape_all(pages=50, delay=0.5):
    session = requests.Session()
    all_products = []
    ts = datetime.utcnow().isoformat()
    
    for p in range(1, pages + 1):
        try:
            items = scrape_page(p, session=session)
            for it in items:
                it["timestamp"] = ts
            all_products.extend(items)
            print(f"[INFO] Page {p} OK ({len(items)} items)")
        except ScrapeError as e:
            print(f"[WARN] Page {p} failed: {e}")

        time.sleep(delay)    
    return all_products