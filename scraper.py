"""
Web Scraper for ScrapeStore E-commerce Website
Scrapes all product data from https://ecommerce-scrape-opal.vercel.app
and saves it as a CSV file matching the existing dataset.csv format exactly.

Uses BeautifulSoup for HTML parsing.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import sys

# Base URL of the website
BASE_URL = "https://ecommerce-scrape-opal.vercel.app"

# CSV headers matching the existing dataset.csv format
CSV_HEADERS = [
    "category_1",
    "category_2",
    "category_3",
    "title",
    "product_rating",
    "selling_price",
    "mrp",
    "seller_name",
    "seller_rating",
    "description",
    "highlights",
    "image_links",
]

# Output file
OUTPUT_FILE = "scraped_dataset.csv"


def get_page_soup(url):
    """Fetch a page and return its BeautifulSoup object."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def scrape_product_card(card):
    """Extract product data from a single product card div."""

    # --- Image link ---
    img_tag = card.find("img")
    image_link = img_tag["src"] if img_tag and img_tag.get("src") else ""

    # --- Title ---
    h3_tag = card.find("h3")
    title = h3_tag.get("title", h3_tag.get_text(strip=True)) if h3_tag else ""

    # --- Product rating ---
    rating_span = card.find("span", class_=lambda c: c and "text-blue-600" in c)
    product_rating = ""
    if rating_span:
        rating_text = rating_span.get_text(strip=True)
        # Remove the star symbol and extract the number
        product_rating = rating_text.replace("\u2605", "").strip()
        if product_rating == "N/A":
            product_rating = ""

    # --- Categories (1 and 2 from visible text) ---
    category_p = card.find("p", class_=lambda c: c and "text-indigo-500" in c)
    category_1 = ""
    category_2 = ""
    if category_p:
        cat_text = category_p.get_text(strip=True)
        # Categories are separated by ">"
        parts = [part.strip() for part in cat_text.split(">")]
        if len(parts) >= 1:
            category_1 = parts[0]
        if len(parts) >= 2:
            category_2 = parts[1]

    # --- Category 3 (from data attribute) ---
    category_3 = card.get("data-category3", "")

    # --- Selling price ---
    price_spans = card.find_all("span", class_=lambda c: c and "font-bold" in c)
    selling_price = ""
    if price_spans:
        selling_price = price_spans[0].get_text(strip=True)

    # --- MRP (original price, line-through) ---
    mrp_span = card.find("span", class_=lambda c: c and "line-through" in c)
    mrp = mrp_span.get_text(strip=True) if mrp_span else ""

    # --- Seller name ---
    seller_p = card.find("p", class_=lambda c: c and "text-gray-500" in c and "truncate" in c)
    seller_name = ""
    if seller_p:
        seller_text = seller_p.get_text(strip=True)
        # Remove "Sold by: " prefix
        if seller_text.startswith("Sold by:"):
            seller_name = seller_text.replace("Sold by:", "").strip()
        else:
            seller_name = seller_text

    # --- Seller rating (from data attribute) ---
    seller_rating = card.get("data-seller-rating", "")

    # --- Description (from data attribute) ---
    description = card.get("data-description", "")

    # --- Highlights (from data attribute) ---
    highlights = card.get("data-highlights", "")

    return {
        "category_1": category_1,
        "category_2": category_2,
        "category_3": category_3,
        "title": title,
        "product_rating": product_rating,
        "selling_price": selling_price,
        "mrp": mrp,
        "seller_name": seller_name,
        "seller_rating": seller_rating,
        "description": description,
        "highlights": highlights,
        "image_links": image_link,
    }


def get_total_pages(soup):
    """Extract total number of pages from the navigation text."""
    nav = soup.find("nav", class_=lambda c: c and "text-gray-600" in c)
    if nav:
        text = nav.get_text(strip=True)
        # Format: "Page X of Y | Total Products: Z"
        if "of" in text:
            parts = text.split("of")
            page_part = parts[1].strip().split("|")[0].strip()
            try:
                return int(page_part)
            except ValueError:
                pass
    return 241  # Default fallback


def scrape_all_pages():
    """Scrape all pages and return a list of product dictionaries."""
    all_products = []

    # First, scrape the homepage (page 1)
    print("Scraping page 1 (homepage)...")
    soup = get_page_soup(BASE_URL)
    if not soup:
        print("Failed to fetch homepage. Exiting.")
        return []

    total_pages = get_total_pages(soup)
    print(f"Total pages to scrape: {total_pages}")

    # Scrape products from page 1
    cards = soup.find_all("div", class_="product-card")
    for card in cards:
        product = scrape_product_card(card)
        all_products.append(product)
    print(f"  Page 1: scraped {len(cards)} products (Total: {len(all_products)})")

    # Scrape remaining pages (page_2.html to page_{total_pages}.html)
    for page_num in range(2, total_pages + 1):
        url = f"{BASE_URL}/site/page_{page_num}.html"
        print(f"Scraping page {page_num}/{total_pages}...", end=" ")

        soup = get_page_soup(url)
        if not soup:
            print(f"FAILED - skipping page {page_num}")
            continue

        cards = soup.find_all("div", class_="product-card")
        for card in cards:
            product = scrape_product_card(card)
            all_products.append(product)

        print(f"scraped {len(cards)} products (Total: {len(all_products)})")

        # Small delay to be polite to the server
        time.sleep(0.3)

    return all_products


def save_to_csv(products, filename):
    """Save the list of product dictionaries to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(products)
    print(f"\nSaved {len(products)} products to '{filename}'")


def main():
    print("=" * 60)
    print("  ScrapeStore Web Scraper")
    print(f"  Target: {BASE_URL}")
    print("=" * 60)
    print()

    # Scrape all products
    products = scrape_all_pages()

    if not products:
        print("No products scraped. Exiting.")
        sys.exit(1)

    # Save to CSV
    save_to_csv(products, OUTPUT_FILE)

    print(f"\nScraping complete!")
    print(f"  Total products: {len(products)}")
    print(f"  Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
