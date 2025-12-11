from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uvicorn
import io

app = FastAPI(title="AI Service", version="0.1")

class TextRequest(BaseModel):
    text: str

@app.post("/v1/classify")
async def classify_text(req: TextRequest):
    # placeholder: simple rule-based demo classifier
    text = req.text.lower()
    if "invoice" in text or "payment" in text:
        label = "finance"
    elif "patient" in text or "medical" in text:
        label = "healthcare"
    elif "order" in text or "sku" in text:
        label = "ecommerce"
    else:
        label = "general"
    return {"label": label, "confidence": 0.6}

@app.post("/v1/summarize")
async def summarize_text(req: TextRequest):
    # trivial summarization: return first 20 words
    words = req.text.split()
    summary = " ".join(words[:20]) + ("..." if len(words) > 20 else "")
    return {"summary": summary}

@app.post("/v1/upload-and-analyze")
async def upload_and_analyze(file: UploadFile = File(...)):
    # simple file type echo + size
    contents = await file.read()
    return {"filename": file.filename, "content_type": file.content_type, "size_bytes": len(contents)}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
