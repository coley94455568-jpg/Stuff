$ErrorActionPreference = "Stop"

python -m pip install pyinstaller
pyinstaller --onefile --windowed --name "Adaptive Revision Timetable" --distpath ".\dist" --workpath ".\build" --specpath "." main.py

Write-Host "Build complete. EXE is in .\dist\Adaptive Revision Timetable.exe"
