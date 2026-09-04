# Project Summary

## Overview

This project is a small command-line-style AI coding agent. It uses the OpenAI Python client to let a language model inspect and modify files in the project directory through a controlled set of tools.

## How it works

`agent.py`:

1. Loads environment variables with `python-dotenv`.
2. Creates an OpenAI client, which expects the relevant API configuration to be available in the environment.
3. Registers three file-management tools with the model:
   - `list_files` — lists entries in a directory.
   - `read_file` — reads a file's contents.
   - `write_file` — writes supplied content to a file.
4. Sends the instruction to inspect the project and create a summary file to the OpenAI Responses API.
5. Repeatedly executes any function calls returned by the model, sends their results back to the model, and continues until the model produces a final text response.

The configured model is `gpt-5.6-luna`.

## File access and safety

The tool implementations live in `tools.py`. They treat the current working directory as the project root and resolve requested paths before accessing them. A path is rejected if it would escape the project directory, preventing the agent from reading or writing outside the project. Files are opened directly for reading and writing; writing replaces the target file's existing contents.

## Dependencies and configuration

`requirements.txt` lists the two Python dependencies:

- `openai` for communication with the Responses API.
- `python-dotenv` for loading environment variables, typically from a `.env` file.

`README.md` currently contains only the project title, so the primary implementation and behavior are defined by `agent.py` and `tools.py`.

## Purpose

The project demonstrates the basic architecture of an AI-assisted coding workflow: give a model narrowly scoped filesystem tools, allow it to inspect the repository, and let it create or update project files based on an instruction.
