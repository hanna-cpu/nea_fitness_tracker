@echo off
REM Starts the Fitness Tracker Reflex app.
REM Activates the project's virtual environment and runs the dev server.

cd /d "%~dp0"

call .venv\Scripts\activate.bat

set REFLEX_USE_NPM=1

cd fitness_tracker
reflex run

pause
