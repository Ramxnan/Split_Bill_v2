@echo off

REM Check if Python is installed
echo Checking if Python is installed...
python-3.12.6\python --version
echo Python is installed...
echo ----------------------------------------

echo Running Streamlit app...
echo You can close this window to stop the app after you are done.
python\python.exe -m streamlit run bill_split_app.py
echo Streamlit app stopped.
echo ----------------------------------------

echo Done.