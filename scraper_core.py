# scraper_core.py

from dataclasses import dataclass
from playwright.sync_api import Page

@dataclass
class Product:
    """
    Modelo de datos para un producto de Amazon.
    En vez de usar un dict suelto, usamos una dataclass tipada.
    """
    product_url: str
    title: str
    price: str

def get_product_details(page: Page, product_url: str) -> Product:
    """
    Usa una 'page' de Playwright para:
      1. Navegar a la URL del producto.
      2. Esperar a que cargue el título.
      3. Extraer título y precio.
      4. Devolver un objeto Product con esos datos.

    Si no encuentra el precio, lo marca como "N/A".
    """
    # Navegar a la URL timeout=60s
    page.goto(product_url, timeout=60000)

    # Esperar que el titulo exista en el DOM
    page.wait_for_selector("span#productTitle", timeout=60000)

    # Título (solo el <span>, no el input hidden)
    title = page.locator("span#productTitle").inner_text().strip()

    # Precio (primer .a-offscreen suele ser el bueno)
    price_locator = page.locator(".a-offscreen").first


    # price = price_locator.inner_text().strip()  ESTA FUNCIONA

    try:
        price = price_locator.inner_text().strip()
    except Exception:
        # Si por lo que sea no hay precio (producto sin stock, formato raro, etc.)
        price = "N/A"

    return Product(
        product_url=product_url,
        title=title,
        price=price
    )
