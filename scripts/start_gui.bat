@echo off
title Music-Makro GUI
cd /d "%~dp0\.."
call venv\Scripts\activate
python app\music_makro_gui.py
pause