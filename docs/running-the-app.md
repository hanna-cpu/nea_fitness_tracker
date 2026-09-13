# Running the Fitness Tracker App

## Prerequisites (one-time setup)

- Python (with the `.venv` virtual environment already created at the project root)
- Node.js LTS — required on Windows because Reflex's default frontend runtime (Bun) has a
  bug running `react-router dev` when no system Node.js is present. Install with:
  ```
  winget install --id OpenJS.NodeJS.LTS
  ```
- Reflex installed in the virtual environment (`pip install reflex`, already done in `.venv`)

## Quick start

Double-click **[run_app.bat](../run_app.bat)** in the project root, or run it from a terminal:

```bash
run_app.bat
```

This activates `.venv` and starts the dev server from the `fitness_tracker/` folder.

## What it does

`run_app.bat` runs, in order:

1. `cd` to the project root (wherever the `.bat` file lives)
2. `.venv\Scripts\activate.bat` — activates the Python virtual environment
3. `set REFLEX_USE_NPM=1` — forces Reflex to use npm/Node.js instead of Bun for the
   frontend (works around the Bun restart bug — see below)
4. `cd fitness_tracker`
5. `reflex run` — compiles and serves the app

## Manual start (equivalent, if you don't want to use the .bat file)

From the project root, in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
$env:REFLEX_USE_NPM = '1'
cd fitness_tracker
reflex run
```

Or in Command Prompt:

```cmd
.venv\Scripts\activate.bat
set REFLEX_USE_NPM=1
cd fitness_tracker
reflex run
```

## URLs

Once running:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

Press `Ctrl+C` in the terminal to stop the server.

## Why `REFLEX_USE_NPM=1` is needed

On Windows, Reflex normally uses **Bun** to run the frontend (`react-router dev`) for
speed. Without a system Node.js install, Bun's own execution of `react-router dev`
trips a restart-guard bug in that tool (`react-router` tries to restart itself with
extra `NODE_OPTIONS` flags, and the restart detection breaks under Bun), causing:

```
error: restartWithMergedOptions() was called, but the process has already been restarted.
```

Installing Node.js and setting `REFLEX_USE_NPM=1` makes Reflex use npm instead of Bun
for the frontend, avoiding that bug entirely.
