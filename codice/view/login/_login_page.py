from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from view.style.ui_style import WidgetRole, WidgetColor


class LoginPage(QWidget):
    """View della pagina per scegliere il tipo di `Account` con cui ingressare all'app."""

    def __init__(self):
        super().__init__()

        self._setup_ui()

    # ------------------------- SETUP INIT -------------------------

    def _setup_ui(self) -> None:
        # Content
        title = QLabel("Tell")
        title.setProperty(WidgetRole.Label.TITLE, True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_login_as_cliente = QPushButton("Accedi")
        self.btn_login_as_cliente.setProperty(WidgetColor.Button.BLUE, True)
        self.btn_login_as_cliente.setProperty(WidgetRole.Button.MAIN, True)

        self.btn_login_with_credentials = QPushButton("Accedi con credenziali")
        self.btn_login_with_credentials.setProperty(WidgetRole.Button.TRASPARENT, True)
        self.btn_login_with_credentials.setMinimumHeight(32)
        font = self.btn_login_with_credentials.font()
        font.setUnderline(True)
        self.btn_login_with_credentials.setFont(font)

        btn_login_credentials_box = QWidget()
        layout_btn_login_box = QHBoxLayout(btn_login_credentials_box)
        layout_btn_login_box.setContentsMargins(0, 1, 0, 1)
        layout_btn_login_box.addStretch()
        layout_btn_login_box.addWidget(self.btn_login_with_credentials)
        layout_btn_login_box.addStretch()

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        main_layout.addStretch()
        main_layout.addWidget(title)
        main_layout.addWidget(self.btn_login_as_cliente)
        main_layout.addSpacing(4)
        main_layout.addWidget(btn_login_credentials_box)
        main_layout.addStretch()
