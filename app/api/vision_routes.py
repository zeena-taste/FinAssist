from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import io
import csv
import json
import google.generativeai as genai
from app.config import settings

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

router = APIRouter()

MODEL_NAME = "gemini-3.1-pro-preview"

VISION_SYSTEM_PROMPT = """You are FinAassist. You extract line-item transactions from images of receipts, logs, or financial statements.
You MUST extract the data exactly as seen in the image accurately.
You MUST return ONLY a valid JSON array of objects, with each object conforming exactly to this structure:
{
    "date": "YYYY-MM-DD",
    "description": "Item or service name",
    "amount": 10.50,
    "category": "expense | income"
}
If no transactions could be found, return empty array [].
Do NOT wrap the JSON in markdown blocks. Just return raw JSON brackets strictly.
"""

@router.post("/upload-receipt")
async def process_receipt(file: UploadFile = File(...)):
    """Receives a multipart image and returns a compiled CSV file streamed back dynamically."""
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key missing.")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
        
    try:
        image_bytes = await file.read()
        mime_type = file.content_type

        model = genai.GenerativeModel(
            MODEL_NAME,
            system_instruction=VISION_SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"}
        )

        image_part = {"mime_type": mime_type, "data": image_bytes}
        response = model.generate_content([
            "Extract all financial transactions from this image neatly converting into JSON format strictly.",
            image_part
        ])
        
        try:
            transactions = json.loads(response.text)
        except (json.JSONDecodeError, Exception):
            transactions = []
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date", "Description", "Amount", "Category"])
        
        for tx in transactions:
            writer.writerow([
                tx.get("date", ""),
                tx.get("description", ""),
                tx.get("amount", "0"),
                tx.get("category", "expense")
            ])
             
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="extracted_transactions.csv"'}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision extraction failed: {str(e)}")
