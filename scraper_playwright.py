from playwright.sync_api import sync_playwright

def get_product_details(product_url: str) -> dict:
    product_details = {}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # pon False si quieres ver el navegador
            page = browser.new_page()

            # Cargar la página
            page.goto(product_url, timeout=60000)
            # Esperar a que el título aparezca
            page.wait_for_selector("span#productTitle", timeout=60000)

            # 🔹 Aquí especificamos el SPAN, no el input hidden
            title = page.locator("span#productTitle").inner_text().strip()

            # 🔹 Precio: usamos el primer .a-offscreen (suele ser el precio visible)
            price_locator = page.locator(".a-offscreen").first
            price = price_locator.inner_text().strip()

            # Rellenar diccionario
            product_details["title"] = title
            product_details["price"] = price
            product_details["product_url"] = product_url

            browser.close()
            return product_details

    except Exception as e:
        print("Could not fetch product details")
        print(f"Failed with exception: {e}")
        return None


# --- EJECUCIÓN ---
product_url = input("Enter product url: ")
product_details = get_product_details(product_url)


print("\n--- PRODUCT DETAILS ---")
for key, value in product_details.items():
    print(f"{key.capitalize()}: {value}")
print("------------------------\n")


