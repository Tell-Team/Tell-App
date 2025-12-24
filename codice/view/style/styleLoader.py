from pathlib import Path

MAIN_QSS_PATH = Path(__file__).parent / "main.qss"


def load_main_stylesheet() -> str:
    with open(MAIN_QSS_PATH, "r") as f:
        return f.read()
