def load_stylesheet(path: str):
    with open(path, "r") as f:
        return f.read()