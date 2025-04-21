@echo off
echo Iniciando servidor Flask...
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
pause
