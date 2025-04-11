@echo off
:: Activate virtual environment
call workon NeuroReconEnv

:: Set environment variable
set ENV_FILE=local.env

:: Start Django development server
python manage.py runserver
