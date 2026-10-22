from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.detector import analyze_url
from backend.response_agent import choose_response

app = FastAPI(title="AI Phishing Detection & Response Agent", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AI Phishing Detection & Response Agent"}

@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    try:
        result = analyze_url(request.url)
        result["response"] = choose_response(result)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
