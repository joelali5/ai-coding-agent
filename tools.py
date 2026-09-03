from pathlib import Path

def list_files(path: str) -> list[str]:
    directory = Path(path)
    return [item.name for item in directory.iterdir()]