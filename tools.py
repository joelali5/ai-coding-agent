from pathlib import Path

def list_files(path: str) -> list[str]:
    directory = Path(path)
    return [item.name for item in directory.iterdir()]

def read_file(path: str) -> str:
    file_path = Path(path)
    with file_path.open("r") as f:
        return f.read()
