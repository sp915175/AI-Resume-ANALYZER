SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "MySQL",
    "FastAPI",
    "Machine Learning",
    "Git",
    "Docker",
    "AWS",
    "React"
]

def extract_skills(text):
    found = []

    text = text.lower()

    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return found