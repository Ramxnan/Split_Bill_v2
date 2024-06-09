@echo off

REM Set the virtual environment name
set VENV_NAME=bill_split_venv

REM Log file location
set LOG_FILE=logs.log

REM Set the date and time for the log file
echo %date% %time% > %LOG_FILE%

REM Check if Python is installed
echo Checking if Python is installed...
python --version >> %LOG_FILE% 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed, installing now...
    echo Python is not installed. Installing Python... >> %LOG_FILE% 2>&1
    REM echo a line onto the console to separate
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ---------------------------------------- 

    REM Download Python installer
    echo Downloading Python installer...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.9.12/python-3.9.12-amd64.exe >> %LOG_FILE% 2>&1
    echo Python installer downloaded successfully.
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ----------------------------------------

    
    REM Install Python silently
    echo Installing Python...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 >> %LOG_FILE% 2>&1
    echo Python installed successfully.
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ----------------------------------------
    
    REM Clean up installer
    del python-installer.exe
    echo Python installer deleted.
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ----------------------------------------
)

echo Python is installed successfully...
echo ---------------------------------------- >> %LOG_FILE% 2>&1
echo ----------------------------------------

REM Check if virtual environment exists
if exist %VENV_NAME% (
    echo Activating existing virtual environment...
    call %VENV_NAME%\Scripts\activate >> %LOG_FILE% 2>&1
    echo Virtual environment activated.
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ----------------------------------------
) else (
    echo Creating virtual environment...
    python -m venv %VENV_NAME% >> %LOG_FILE% 2>&1
    echo Virtual environment created successfully.
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ----------------------------------------

    echo Activating virtual environment...
    call %VENV_NAME%\Scripts\activate >> %LOG_FILE% 2>&1
    echo Virtual environment activated.
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ----------------------------------------

    echo Upgrading pip...
    python -m pip install --upgrade pip >> %LOG_FILE% 2>&1
    echo Pip upgraded successfully.
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ----------------------------------------

    echo Installing dependencies...
    pip install -r requirements.txt >> %LOG_FILE% 2>&1
    echo Dependencies installed successfully.
    echo ---------------------------------------- >> %LOG_FILE% 2>&1
    echo ----------------------------------------
)

echo Running Streamlit app...
echo You can close this window to stop the app after you are done.
streamlit run bill_split_app.py >> %LOG_FILE% 2>&1
echo Streamlit app stopped.
echo ---------------------------------------- >> %LOG_FILE% 2>&1
echo ----------------------------------------

echo Deactivating virtual environment...
deactivate
echo Virtual environment deactivated.
echo ---------------------------------------- >> %LOG_FILE% 2>&1
echo ----------------------------------------

echo Done.