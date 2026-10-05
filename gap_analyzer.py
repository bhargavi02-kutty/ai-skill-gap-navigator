# gap_analyzer.py

def calculate_skill_gap(student_skills, target_skills):

    results = []

    for skill, importance in target_skills.items():

        current_level = student_skills.get(skill, 0)

        gap = importance - current_level

        if gap < 0:
            gap = 0

        if gap == 0:
            status = "Strong"
        elif gap <= 3:
            status = "Needs Improvement"
        elif gap <= 6:
            status = "Moderate Gap"
        else:
            status = "Major Gap"

        results.append({
            "Skill": skill,
            "Importance": importance,
            "Current Level": current_level,
            "Gap": gap,
            "Status": status
        })

    results.sort(key=lambda x: x["Gap"], reverse=True)

    return results