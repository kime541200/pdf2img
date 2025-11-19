import shutil
import tempfile
import zipfile
import os
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from .core import a_convert_pdf_to_images

app = FastAPI(title="PDF2Img Server")

def _cleanup_temp_dir(path: str):
    shutil.rmtree(path, ignore_errors=True)

@app.post("/convert")
async def convert_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    fmt: str = "png",
    dpi: int = 200
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Create a temp directory for this request
    temp_dir = tempfile.mkdtemp()
    input_pdf_path = Path(temp_dir) / file.filename
    output_images_dir = Path(temp_dir) / "images"
    
    try:
        # Save uploaded file
        with open(input_pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Convert
        await a_convert_pdf_to_images(input_pdf_path, output_images_dir, fmt, dpi)
        
        # Zip results
        zip_path = Path(temp_dir) / "result.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(output_images_dir):
                for f in files:
                    zipf.write(os.path.join(root, f), f)
        
        # Schedule cleanup
        background_tasks.add_task(_cleanup_temp_dir, temp_dir)
        
        return FileResponse(
            zip_path, 
            media_type="application/zip", 
            filename=f"{Path(file.filename).stem}_images.zip"
        )

    except Exception as e:
        _cleanup_temp_dir(temp_dir)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

