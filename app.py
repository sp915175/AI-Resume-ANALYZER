from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import shutil
import os

from utils.pdf_parser import extract_text
from utils.skill_extractor import extract_skills
from utils.ats_score import calculate_ats_score
from utils.missing_skills import get_missing_skills

app = FastAPI(title="AI Resume Analyzer")

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Allow only PDF
        if not file.filename.lower().endswith(".pdf"):
            return {
                "error": "Please upload a PDF resume."
            }

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        resume_text = extract_text(file_path)

        # Extract skills
        skills = extract_skills(resume_text)

        # ATS Score
        ats_score = calculate_ats_score(skills)

        # Missing Skills
        missing_skills = get_missing_skills(skills)

        return {
            "filename": file.filename,
            "skills": skills,
            "missing_skills": missing_skills,
            "ats_score": ats_score,
            "resume_text": resume_text
        }

    except Exception as e:
        return {
            "error": str(e)
        }