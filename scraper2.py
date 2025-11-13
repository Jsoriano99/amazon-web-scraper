from playwright.sync_api import sync_playwright

def get_product_details(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        title = page.locator('#productTitle').inner_text().strip()
        price = page.locator('.a-offscreen').first.inner_text().strip()

        return {
            "title": title,
            "price": price,
            "url": url
        }

print(get_product_details("https://www.amazon.com/Acer-Chromebook-Graphics-802-11ac-CB512-C1KJ/dp/B0DNTDX72K?th=1"))
