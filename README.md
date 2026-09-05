# AI Coding Agent

A small command-line AI coding agent that uses the OpenAI Responses API to inspect and modify files in the current project directory. The agent receives a user's request, decides which filesystem or Python-execution tools it needs, runs those tools locally, and continues until it can provide a final response.

## Features

- Lists files in the project directory.
- Reads and writes project files.
- Replaces one exact occurrence of text in a file.
- Runs Python files with captured standard output, standard error, and exit status.
- Restricts file paths to the project root.
- Stops after a maximum of 10 model/tool iterations.

## Project structure

| File                    | Purpose                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| `agent.py`              | Command-line entry point, OpenAI client setup, tool definitions, and the model/tool-calling loop. |
| `tools.py`              | Local implementations of the file and Python-execution tools.                                     |
| `simple_greeting.py`    | Minimal example Python file that prints `Hello, world!`.                                          |
| `project_summary.md`    | Existing summary of the project and its intended architecture.                                    |
| `requirements.txt`      | Python dependencies: `openai` and `python-dotenv`.                                                |
| `.gitignore`            | Excludes virtual-environment files, environment files, caches, and coverage output.               |
| `.vscode/settings.json` | Configures the workspace to use `.venv/bin/python` as the default interpreter.                    |

## Requirements

- Python 3.9 or newer is recommended.
- An OpenAI API key and access to the configured model.
- Internet access for OpenAI API requests.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Configure the OpenAI client. The project loads variables from a `.env` file, and the OpenAI Python client expects `OPENAI_API_KEY`:

   ```dotenv
   OPENAI_API_KEY=your_api_key_here
   ```

   Do not commit `.env`; it is excluded by `.gitignore`. The model is currently hard-coded in `agent.py` as `gpt-5.6-luna`, so that model must be available to the configured account. Change the `model` argument in `agent.py` if a different model is required.

## Usage

Run the agent from the project root:

```bash
python agent.py
```

Enter a natural-language request when prompted, for example:

```text
Review simple_greeting.py and explain what it does.
```

The model may inspect files, modify them, or run Python files depending on the request. Its final response is printed to the terminal.

The example file can also be run directly:

```bash
python simple_greeting.py
```

## Available tools

The model can call the following tools:

- **`list_files(path)`** — returns the names of entries in a directory.
- **`read_file(path)`** — returns the complete contents of a file.
- **`write_file(path, content)`** — replaces a file's contents, or creates it if the parent directory already exists.
- **`run_python_file(path)`** — runs a `.py` file for up to five seconds and returns `stdout`, `stderr`, and `returncode`. Non-Python files are rejected.
- **`replace_in_file(path, old_text, new_text)`** — replaces exactly one occurrence of `old_text`; it fails if the text is missing or occurs more than once.

All paths are resolved relative to the process's current working directory (`Path.cwd()`). Paths that resolve outside that directory are rejected. Run the command from the intended project root, and remember that the agent can modify files without an additional confirmation step.

## How the agent works
1. `agent.py` loads `.env` values with `python-dotenv`.
2. It creates an `OpenAI` client and prompts for the user's request.
3. It sends the request, agent instructions, and tool schemas to the Responses API.
4. It executes returned function calls locally and sends their results back using the response ID.
5. It repeats this process until the model returns text or 10 iterations have been reached.
6. Tool exceptions are returned to the model as error objects so it can respond or recover where possible.

## Development notes
Keep the working directory at the repository root when running the agent. To add or change a tool, update both its implementation in `tools.py` and its schema and registry entry in `agent.py`. When changing the tool contract, keep the function signature, schema, and documentation synchronized.
