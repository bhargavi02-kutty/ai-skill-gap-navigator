# roadmap.py

def generate_roadmap(gap_results):

    roadmap = []

    for item in gap_results:

        skill = item["Skill"]
        gap = item["Gap"]

        if gap == 0:
            continue

        if gap >= 7:
            level = "Beginner"
            duration = "3-4 weeks"

        elif gap >= 4:
            level = "Intermediate"
            duration = "2-3 weeks"

        else:
            level = "Revision"
            duration = "1-2 weeks"

        roadmap.append({
            "Skill": skill,
            "Level": level,
            "Duration": duration
        })

    return roadmap