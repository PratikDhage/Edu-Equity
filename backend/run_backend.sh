cd ~/edu-equity-local/backend
source ../venv/bin/activate
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --log-level debug
