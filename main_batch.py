# main_batch.py

from browser_manager import BrowserManager
from scraper_core import get_product_details
from io_utils import read_urls_from_file, save_products_to_csv

def run_batch(input_file: str = "urls.txt", output_file: str = "products.csv"):
    """
    Pipeline principal para scraping en batch:

    1. Leer URLs desde un archivo de texto (input_file).
    2. Abrir navegador con Playwright (una sola vez).
    3. Recorrer cada URL:
        - Navegar a la página del producto.
        - Extraer título y precio.
        - Acumular resultados.
    4. Guardar todos los productos en un CSV (output_file).
    """
    # Leemos todas las urls del archivo
    urls = read_urls_from_file(input_file)

    # Lista donde iremos guardando los objetos Product.
    products = []

    # Abrimos el navegador usando nuestro BrowserManager.
    with BrowserManager(headless=True) as page:
        for url in urls:
            try:
                print(f"Scrapeando: {url}")
                product = get_product_details(page, url)
                products.append(product)
                print(f"OK -> {product.title}")
            except Exception as e:
                print(f"[ERROR] {url}: {e}")

    save_products_to_csv(products, output_file)
    print(f"\nScraping terminado. {len(products)} productos guardados en {output_file}")

if __name__ == "__main__":
    run_batch()
