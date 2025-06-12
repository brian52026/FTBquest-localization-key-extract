# AGENTS Guidelines

This repository contains scripts to extract localization keys from FTB quests and refill them after translation. Below are guidelines for contributors and tooling.

## Project Components

- `extract_quest.py` – Parses `.snbt` files and outputs sanitized quest files along with `outdict.json` for translation.
- Translation JSON – The `outdict.json` file generated in `out_chapters` holds the extracted strings. Translators update this file with translated text.
- `refill_quest.py` – Reads a directory with `outdict.json` and inserts translations back into the quest files.
- Command line interface – Both scripts are run from the command line by providing the path to a folder of quest files.
- Tests – Located under the `tests` directory and written with `unittest` to verify extraction and refilling functions.

## Coding Standards

- Target **Python 3.10+**.
- Follow **PEP-8** with a maximum line length of **100 characters**.
- Use **type hints** for all function signatures and include **docstrings** describing purpose, parameters and return values.

## Running Tests

Execute the test suite from the repository root with:

```bash
python -m unittest
```

## Commit and Pull Request Guidelines

- Squash related changes into a **single concise commit**.
- Provide a brief and clear summary when opening a pull request.


