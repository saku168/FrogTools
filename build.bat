@echo off
python -m pip install --upgrade pip
python -m pip install pyinstaller
python -m PyInstaller --onefile --name FrogTools frogtools.py
echo.
echo Done. Check dist\FrogTools.exe
pause
