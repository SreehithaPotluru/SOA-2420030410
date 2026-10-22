# AI-Based Phishing Detection & Response Agent

## Features
- Web interface to submit a URL.
- Explainable starter URL checks and risk score.
- Response-agent recommendation: allow with caution, warn, or simulated block/alert.
- FastAPI backend.
- Optional Random Forest training script for a CSV containing `url,label`.

## Important limitation
The included detector is a transparent heuristic baseline; it is not the original trained PhiUSIIL model. Risk scores are indicators, not calibrated probabilities. The response agent simulates blocking and does not block traffic, report URLs externally, or quarantine emails.

## Run on Windows (VS Code terminal)
From the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

Keep the backend terminal running. Open a second terminal and serve the frontend:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://127.0.0.1:5500` in your browser. API docs: `http://127.0.0.1:8000/docs`.

## Optional model training
Create `data/urls.csv` with headers `url,label`, where `1` means legitimate and `0` means phishing, then run:

```bash
python scripts/train_model.py --csv data/urls.csv
```

Training creates `backend/model/phishing_model.joblib`. This starter version does not automatically load that model in the API; integration must use the same feature columns and class-label mapping.
