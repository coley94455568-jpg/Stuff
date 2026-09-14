@echo off
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name "Adaptive Revision Timetable" --distpath ".\dist" --workpath ".\build" --specpath "." main.py

echo.
echo Build complete.
echo EXE location: .\dist\Adaptive Revision Timetable.exe
pause
