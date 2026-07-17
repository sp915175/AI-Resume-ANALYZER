def calculate_ats_score(skills):

    total_skills = 15   # हमारी SKILLS list में 15 skills हैं

    score = (len(skills) / total_skills) * 100

    return round(score)