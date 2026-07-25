from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from utils.pdf_parser import extract_text
from utils.skill_extractor import extract_skills
from utils.ats_score import calculate_ats_score
from utils.missing_skills import get_missing_skills

app = FastAPI(title="AI Resume Analyzer")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "request": request
    }
)

@app.post("/upload")
async def upload_resume(resume: UploadFile = File(...)):
    # PDF text निकालो
    resume_text = extract_text(resume.file)
    # Skills निकालो
    skills = extract_skills(resume_text)

    # ATS Score निकालो
    ats_score = calculate_ats_score(skills)

    # Missing Skills निकालो
    missing_skills = get_missing_skills(skills)

    # Strengths
    strengths = []

    if "Python" in skills:
        strengths.append("Good Python knowledge")

    if "SQL" in skills:
        strengths.append("Knows SQL")

    if "Java" in skills:
        strengths.append("Has Java knowledge")

    if "Communication" in skills:
        strengths.append("Good communication skills")

    # Suggestions
    suggestions = []

    if "Docker" in missing_skills:
        suggestions.append("Learn Docker")

    if "AWS" in missing_skills:
        suggestions.append("Learn AWS")

    if "Git" in missing_skills:
        suggestions.append("Learn Git")

    if "Machine Learning" in missing_skills:
        suggestions.append("Learn Machine Learning")

    # Resume Summary
    if ats_score >= 80:
        summary = "Excellent Resume. Ready for most software developer roles."

    elif ats_score >= 60:
        summary = "Good Resume. Add a few missing skills to improve your chances."

    else:
        summary = "Resume needs improvement. Add more technical skills and projects."

    return {
        "filename": resume.filename,
        "skills": skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
        "strengths": strengths,
        "suggestions": suggestions,
        "resume_summary": summary,
        "text": resume_text
    }