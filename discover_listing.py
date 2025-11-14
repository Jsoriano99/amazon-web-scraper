from typing import List
from browser_manager import BrowserManager
from io_utils import read_urls_from_file
from urllib.parse import urljoin
from browser_manager import BrowserManager
from urllib.parse import urljoin

def extract_product_urls_from_listing(listing_url: str, max_products: int = 50):
    urls = []

    with BrowserManager(headless=False) as page:
        try:
            # 1) Cargar la página
            page.goto(listing_url, timeout=60000)
            page.wait_for_selector("div.s-main-slot", timeout=60000)
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el listado {listing_url}: {e}")
            return []

        # 2) Bloques de productos
        results = page.locator(
            "div.s-main-slot div[data-asin][data-component-type='s-search-result']"
        )
        print("Bloques de resultados encontrados:", results.count())

        results_count = results.count()
        total = min(results_count, max_products)

        # 3) Extraer enlaces por BLOQUE
        for i in range(total):
            result = results.nth(i)

            asin = result.get_attribute("data-asin")
            print(f"[DEBUG] Producto #{i} – ASIN: {asin}")

            # buscar el enlace principal del producto dentro de su propio bloque
            link = result.locator("a.a-link-normal[href*='/dp/']").first
            href = link.get_attribute("href")
            print("DEBUG href crudo:", href)

            if not href:
                continue

            full_url = urljoin(listing_url, href)
            urls.append(full_url)

        # 5) Eliminar duplicados
        urls = list(dict.fromkeys(urls))   # mantiene orden y elimina duplicados
        print(f"[DEBUG] URLs finales sin duplicados: {len(urls)}")

    # 6) Fuera del WITH
    return urls


if __name__ == "__main__":
    listing_url = "https://www.amazon.es/s?k=iphone+16"
    urls = extract_product_urls_from_listing(listing_url, max_products=5)

    print("\nPRODUCTOS ENCONTRADOS:")
    for u in urls:
        print(u)



