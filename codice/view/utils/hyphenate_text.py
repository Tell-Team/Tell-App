from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
import re
from typing import Optional, override


def _soft_hyphenate_html(text: str, step: int = 1) -> str:  # alt: step = 6
    """Separa con un trattino le parole che non rientrano nella QLabel che le contiene.
    Non è grammaticalmente corretto. Solo separa testo, lasciando i tags intatti."""

    # https://pypi.org/project/pyphen/ sarebbe utile se questo fosse importante.
    if not text:
        return ""

    parts = re.split(r"(<[^>]+>)", text)

    def hyphenate_word(word: str) -> str:
        return "\u00ad".join(word[i : i + step] for i in range(0, len(word), step))

    for i, part in enumerate(parts):
        if not part.startswith("<"):
            tokens = re.split(r"(\s+)", part)
            parts[i] = "".join(
                hyphenate_word(t) if not t.isspace() else t for t in tokens
            )

    return "<html><body>" + "".join(parts) + "</body></html>"


class HyphenatedLabel(QLabel):
    """Label che applica automaticamente la sillabazione al testo."""

    def __init__(self, text: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWordWrap(True)
        self.setTextFormat(Qt.TextFormat.RichText)
        self._raw_text = text or ""
        self.setText(self._raw_text)

    @override
    def text(self) -> str:
        return self._raw_text

    @override
    def setText(self, a0: Optional[str] = None) -> None:
        self._raw_text = a0 or ""
        super().setText(_soft_hyphenate_html(self._raw_text))
