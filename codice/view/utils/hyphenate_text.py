from PyQt6.QtWidgets import QLabel
from typing import Optional, override


def _soft_hyphenate(text: str, step: int = 1):  # alt: step = 6
    """Separa con un trattino le parole che non rientrano nella QLabel che le contiene.
    Non è grammaticalmente corretto."""

    # https://pypi.org/project/pyphen/ sarebbe utile se questo fosse importante.
    if not text:
        return ""
    return " ".join(
        "\u00ad".join(word[i : i + step] for i in range(0, len(word), step))
        for word in text.split()
    )


class HyphenatedLabel(QLabel):
    """Label che applica automaticamente la sillabazione al testo."""

    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__()
        self.setWordWrap(True)
        self._raw_text = text or ""
        self.setText(self._raw_text)

    @override
    def text(self) -> str:
        return self._raw_text

    @override
    def setText(self, a0: Optional[str] = None) -> None:
        self._raw_text = a0 or ""
        super().setText(_soft_hyphenate(self._raw_text))
