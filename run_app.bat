@echo off

REM Set the virtual environment name
set VENV_NAME=bill_split_venv

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...
    
    REM Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.9.12/python-3.9.12-amd64.exe
    
    REM Install Python silently
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    REM Clean up installer
    del python-installer.exe
)

REM Check if virtual environment exists
if exist %VENV_NAME% (
    echo Activating existing virtual environment...
) else (
    echo Creating virtual environment...
    python -m venv %VENV_NAME%
    
    REM Activate virtual environment
    call %VENV_NAME%\Scripts\activate
    
    REM Upgrade pip
    python -m pip install --upgrade pip

    REM Install dependencies
    pip install -r requirements.txt
    
    REM Deactivate virtual environment after installing requirements
    deactivate
)

REM Activate virtual environment
call %VENV_NAME%\Scripts\activate

REM Run the Streamlit app
streamlit run bill_split_app.py

REM Deactivate virtual environment
deactivate

pause
