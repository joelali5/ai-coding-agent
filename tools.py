from pathlib import Path
import subprocess

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


def write_file(path: str, content: str) -> str:
    file_path = get_safe_path(path)
    with file_path.open("w") as f:
        f.write(content)
    return f"Successfully wrote to {file_path}"

def run_python_file(path: str) -> dict:
    file_path = get_safe_path(path)
    if file_path.suffix != ".py":
        raise ValueError("Only Python files can be executed.")
    result = subprocess.run(["python", str(file_path)], capture_output=True, text=True)

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

def replace_in_file(path: str, old_text: str, new_text: str ) -> str:
    file_path = get_safe_path(path)
    with file_path.open("r") as f:
        content = f.read()

    occurrences = content.count(old_text)

    if occurrences == 0:
        raise ValueError(f"{old_text} not found in {file_path}")
    elif occurrences > 1:
        raise ValueError(f"Only a single occurence of {old_text} can be replaced at a time.")

    content = content.replace(old_text, new_text)
    with file_path.open("w") as f:
        f.write(content)

    return f"Successfully replaced {old_text} with {new_text} in {file_path}"