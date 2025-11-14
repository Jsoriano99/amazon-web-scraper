# io_utils.py

from typing import List
import csv
from scraper_core import Product

def read_urls_from_file(path: str) -> List[str]:
    """
    Lee un archivo de texto con URLs (una por línea) y devuelve una lista de strings.

    - Soporta archivos en UTF-16 LE (caso actual) y UTF-8.
    - Limpia posibles caracteres nulos (\x00) y BOM (\ufeff).
    - Ignora líneas vacías.
    """
    # Leemos el archivo en binario para poder elegir la decodificación
    with open(path, "rb") as f:
        raw = f.read()

    text = None

    # 1) Intentar UTF-16 LE primero (como guarda tu VSCode)
    try:
        text = raw.decode("utf-16-le")
        print("[DEBUG] Archivo leído como UTF-16 LE")
    except UnicodeDecodeError:
        pass

    # 2) Si falla, intentar UTF-16 genérico
    if text is None:
        try:
            text = raw.decode("utf-16")
            print("[DEBUG] Archivo leído como UTF-16 (auto)")
        except UnicodeDecodeError:
            pass

    # 3) Si sigue fallando, intentar UTF-8
    if text is None:
        try:
            text = raw.decode("utf-8")
            print("[DEBUG] Archivo leído como UTF-8")
        except UnicodeDecodeError:
            text = raw.decode("utf-8", errors="ignore")
            print("[DEBUG] Archivo leído como UTF-8 (ignore errors)")

    urls: List[str] = []

    for raw_line in text.splitlines():
        print("DEBUG URL LINE:", repr(raw_line))

        # limpiar nulos y BOM
        clean_line = raw_line.replace("\x00", "").strip()
        clean_line = clean_line.lstrip("\ufeff")

        if not clean_line:
            print("Saltando línea vacía:", repr(raw_line))
            continue

        urls.append(clean_line)

    return urls


def save_products_to_csv(products: List[Product], path: str) -> None:
    """Guarda una lista de Product en CSV."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_url", "title", "price"])

        # escribe una fila por producto
        for p in products:
            writer.writerow([p.product_url, p.title, p.price])
