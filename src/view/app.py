import flet as ft
from logging import basicConfig, ERROR
from src.controller.cnab import Cnab
import os

basicConfig(filename='main.log', level=ERROR,
            format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.file_path = None
        self.setup_page()
        self.setup_components()
        self.build_interface()

    def setup_page(self) -> None:
        # Configurações básicas da página
        self.page.title = 'CNAB Reader'
        self.page.window.icon = 'icons\\icon.ico'
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.maximizable = False
        self.page.window.resizable = False
        self.page.window.center()
        self.page.window.to_front()
        self.page.window.height = 420
        self.page.window.width = 535
        self.page.padding = 0
        self.page.bgcolor = ft.colors.with_opacity(
            0.98, ft.colors.SURFACE_VARIANT)
        self.page.fonts = {
            "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"}
        self.page.theme = ft.Theme(font_family="Poppins")
        self.page.update()

    def setup_components(self) -> None:
        # Componentes de seleção de arquivo
        self.file_picker = ft.FilePicker(on_result=self.pick_file)
        self.page.overlay.append(self.file_picker)

        # Ícone e texto de arquivo
        self.file_icon = ft.Icon(
            name=ft.icons.INSERT_DRIVE_FILE_OUTLINED, size=32, color=ft.colors.OUTLINE)
        self.selected_file_text = ft.Text("Nenhum arquivo selecionado", size=14, weight=ft.FontWeight.W_500,
                                          overflow=ft.TextOverflow.ELLIPSIS)

        # Card de arquivo
        self.file_card = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        self.file_icon,
                        ft.Container(content=self.selected_file_text,
                                     expand=True, margin=ft.margin.only(left=10))
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=16
            ),
            elevation=0,
            color=ft.colors.SURFACE_VARIANT,
            margin=ft.margin.only(bottom=20)
        )

        # Botões
        self.select_button = ft.ElevatedButton(
            content=ft.Row([ft.Icon(ft.icons.UPLOAD, ft.Colors.WHITE),
                           ft.Text("Selecionar Arquivo", size=14, weight=ft.FontWeight.W_500)], tight=True),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_400,
            ),
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=["ret"])
        )

        self.process_button = ft.ElevatedButton(
            content=ft.Row([ft.Icon(ft.icons.PLAY_ARROW_ROUNDED, ft.Colors.WHITE),
                           ft.Text("Processar Arquivo", size=14, weight=ft.FontWeight.W_500)], tight=True),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=24, vertical=15),
                color=ft.colors.WHITE,
                bgcolor=ft.colors.GREEN_600,
            ),
            on_click=self.process_file,
            disabled=True
        )

    def pick_file(self, e: ft.FilePickerResultEvent) -> None:
        if e.files:
            self.file_path = e.files[0].path
            self.selected_file_text.value = e.files[0].name
            self.process_button.disabled = False
            self.file_card.border = ft.border.all(2, ft.colors.PRIMARY)
            self.file_icon.color = ft.colors.PRIMARY
        else:
            self.file_path = None
            self.selected_file_text.value = "Nenhum arquivo selecionado"
            self.process_button.disabled = True
            self.file_card.border = ft.border.all(1, ft.colors.OUTLINE)
            self.file_icon.color = ft.colors.OUTLINE
        self.page.update()

    def process_file(self, e) -> None:
        if self.file_path:
            processor = Cnab(self.file_path)
            processor.process()

    def create_panel_section(self, title, content):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                content
            ], spacing=0),
            bgcolor=ft.colors.SURFACE,
            border_radius=12,
            padding=24,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=14,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                offset=ft.Offset(0, 3),
            )
        )

    def build_interface(self) -> None:
        # Cria seções do painel
        file_section = self.create_panel_section("Arquivo", self.file_card)
        actions_section = self.create_panel_section("Ações",
                                                    ft.Row([self.select_button, self.process_button], spacing=20))

        # Painel principal
        panel = ft.Container(
            content=ft.Column([
                file_section,
                ft.Container(height=24),
                actions_section
            ], spacing=0),
            padding=24,
            expand=True
        )

        self.page.add(panel)
