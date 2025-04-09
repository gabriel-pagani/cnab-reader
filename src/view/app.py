import flet as ft
from logging import basicConfig, ERROR


basicConfig(filename='main.log', level=ERROR,
            format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.setup_page()
        self.show_interface()

    def setup_page(self) -> None:
        self.page.title = 'CNAB Reader'
        self.page.window.icon = 'icons\\icon.ico'
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.maximized = True
        self.page.update()

    def show_interface(self) -> None:
        ...
