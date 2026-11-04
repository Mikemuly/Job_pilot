def score_job(skills: str, job_text: str) -> dict:
    skill_list = [s.strip().lower() for s in skills.split(",") if s.strip()]
    text = job_text.lower()

    matched = [s for s in skill_list if s in text]
    score = round(100 * len(matched) / len (skill_list)) if skill_list else 0

    return {"score": score, "matched": matched}

if __name__ == "__main__":
    print(score_job("Python,FastAPI, Docker", "We need a Python dev who knows Docker"))