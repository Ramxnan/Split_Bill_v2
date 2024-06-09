
REM Set the virtual virtual environment name
set VENV_NAME=bill_split_venv

REM Log file location
set LOG_FILE=logs.log

REM set the date and time for the log file
echo %date% %time% > %LOG_FILE%

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python... >> %LOG_FILE% 2>&1
    
    REM Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.9.12/python-3.9.12-amd64.exe >> %LOG_FILE% 2>&1
    
    REM Install Python silently
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 >> %LOG_FILE% 2>&1
    
    REM Clean up installer
    del python-installer.exe
)

REM Check if virtual environment exists
if exist %VENV_NAME% (
    echo Activating existing virtual environment... >> %LOG_FILE% 2>&1
) else (
    echo Creating virtual environment... >> %LOG_FILE% 2>&1
    python -m venv %VENV_NAME% >> %LOG_FILE% 2>&1
    
    REM Activate virtual environment
    call %VENV_NAME%\Scripts\activate
    
    REM Upgrade pip
    python -m pip install --upgrade pip >> %LOG_FILE% 2>&1

    REM Install dependencies
    pip install -r requirements.txt >> %LOG_FILE% 2>&1
    
    REM Deactivate virtual environment after installing requirements
    deactivate
)

REM Activate virtual environment
call %VENV_NAME%\Scripts\activate

REM Run the Streamlit app and log errors
streamlit run bill_split_app.py >> %LOG_FILE% 2>&1

REM Deactivate virtual environment
deactivate

pause
