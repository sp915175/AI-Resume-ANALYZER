from utils.skill_extractor import SKILLS

def get_missing_skills(found_skills):
    missing = []

    for skill in SKILLS:
        if skill not in found_skills:
            missing.append(skill)

    return missing