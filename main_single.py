# main_single.py

from browser_manager import BrowserManager
from scraper_core import get_product_details

if __name__ == "__main__":
    url = input("Enter product url: ").strip()

    with BrowserManager(headless=False) as page:
        product = get_product_details(page, url)

    print("\n--- PRODUCT DETAILS ---")
    print(f"Title: {product.title}")
    print(f"Price: {product.price}")
    print(f"URL:   {product.product_url}")
    print("------------------------\n")
