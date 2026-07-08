# AGENTS.md — Repository instructions for coding agents

Purpose
- Help AI coding agents quickly understand how to run, test, and explore this codebase with minimal noise.

Quick environment & run
- Python environment: create a venv and install dependencies from `requirements.txt`.
- Install: `python -m venv .venv && .venv\\Scripts\\activate && pip install -r requirements.txt`
- Run UI: `python main.py` (entrypoint).
- Tests: `pytest -q` (tests live under `tests/`).

Key locations
- `main.py`: application entrypoint.
- `core/`: business logic, DB access, settings, backup utilities.
- `models/`: data models for songs, artists, records, programs.
- `services/`: service-layer operations used by the UI.
- `ui/`: PySide6 UI pages and windows.
- `tests/`: unit tests; run with `pytest`.

What agents should do first
- Run the test suite and report failures before making changes.
- Open [core/database.py](core/database.py) and [core/crud_engine.py](core/crud_engine.py) for DB patterns.
- Inspect [main.py](main.py) to see application startup and config loading.

Conventions & guardrails
- Prefer small, focused changes and keep public APIs stable.
- Link to existing docs rather than copying large sections; use the repository files named above.
- Tests are the signal of correctness: add or update tests when behavior changes.

Useful commands
- Activate venv (Windows PowerShell):
  - `python -m venv .venv`
  - `.\.venv\\Scripts\\Activate.ps1`
- Install deps: `pip install -r requirements.txt`
- Run tests: `pytest -q`

When adding agent customizations
- Prefer adding or updating `AGENTS.md` at project root.
- If tighter GitHub integration is needed, create `.github/copilot-instructions.md` and keep it synced with this file.

Links
- Project README: [README.md](README.md)
