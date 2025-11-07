python -m venv .venv

call .venv\Scripts\activate
python -m pip install --upgrade pip

pip install -r requirements.txt
echo     .venv\Scripts\activate

@echo off
call .venv\Scripts\activate
uvicorn app:app --reload
pause
