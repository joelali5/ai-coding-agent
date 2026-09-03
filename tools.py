from pathlib import Path

PROJECT_ROOT = Path.cwd()

def get_safe_path(path: str) -> Path:
    requested_path = (PROJECT_ROOT / path).resolve()

    try:
        requested_path.relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        raise ValueError("Access outside the project directory is not allowed.")

    return requested_path

def list_files(path: str) -> list[str]:
    directory = get_safe_path(path)
    return [item.name for item in directory.iterdir()]

def read_file(path: str) -> str:
    file_path = get_safe_path(path)
    with file_path.open("r") as f:
        return f.read()


# print(read_file("agent.py"))
print(read_file("../test-proj"))