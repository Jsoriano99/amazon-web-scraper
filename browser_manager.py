# browser_manager.py

from playwright.sync_api import sync_playwright

class BrowserManager:
    """
    Pequeño wrapper para gestionar Playwright con 'with'.

    Uso:
        from browser_manager import BrowserManager

        with BrowserManager(headless=True) as page:
            page.goto("https://www.amazon.es")
            ...

    - Abre Playwright y el navegador al entrar en el contexto (__enter__).
    - Cierra navegador y Playwright automáticamente al salir (__exit__).
    """

    def __init__(self, headless: bool = True):
        # Si headless=True => navegador sin ventana.
        # Si headless=False => se abre la ventana del navegador (útil para debug).
        self.headless = headless
        self._playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        # Arranca Playwright y abre un navegador Chromium con una pestaña.
        self._playwright = sync_playwright().start()
        self.browser = self._playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        # Devolvemos la página para usarla directamente en el 'with'.
        return self.page

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Se llama automáticamente al salir del 'with' (haya error o no).
        # Cerramos el navegador y paramos Playwright si están abiertos.
        if self.browser:
            self.browser.close()
        if self._playwright:
            self._playwright.stop()
