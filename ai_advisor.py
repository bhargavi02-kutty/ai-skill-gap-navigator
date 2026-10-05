import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# LOAD .ENV FILE
# --------------------------------------------------

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

def get_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not being loaded from .env"
        )

    return genai.Client(api_key=api_key)


# --------------------------------------------------
# AI CAREER ADVISOR
# --------------------------------------------------

def generate_ai_advice(
    name,
    branch,
    year,
    target_role,
    gap_results
):

    client = get_gemini_client()

    # ----------------------------------------------
    # PREPARE SKILL INFORMATION
    # ----------------------------------------------

    skill_information = ""

    for item in gap_results:

        skill_information += (
            f"Skill: {item['Skill']}\n"
            f"Current Level: {item['Current Level']}/10\n"
            f"Gap: {item['Gap']}\n"
            f"Importance: {item['Importance']}/10\n"
            f"Status: {item['Status']}\n\n"
        )

    # ----------------------------------------------
    # PROMPT
    # ----------------------------------------------

    prompt = f"""
You are an AI Career Advisor for B.Tech students.

Student Profile:

Name: {name}
Branch: {branch}
Year: {year}
Target Job Role: {target_role}

Skill Gap Analysis:

{skill_information}

Analyze the student's profile carefully.

Provide personalized career guidance based ONLY
on the provided skill-gap information.

Include:

## 1. Overall Assessment

Explain the student's current position
towards the target job role.

## 2. Top 3 Skills to Focus On

Identify the three most important skills
the student should learn next.

For each skill explain:

- Why the skill is important
- Current skill level
- Skill gap
- What the student should learn

## 3. 30-Day Learning Roadmap

Create a practical week-by-week roadmap.

Week 1:
Foundation

Week 2:
Core concepts

Week 3:
Practical implementation

Week 4:
Project and revision

## 4. Project Ideas

Suggest two practical projects suitable
for this B.Tech student.

## 5. Interview Preparation

Give five interview questions related
to the student's important skill gaps.

## 6. Motivation

Give one short motivational message.

Important instructions:

- Do not invent the student's skill levels.
- Use only the provided skill-gap information.
- Prioritize skills with high importance
  and large gaps.
- Make the roadmap realistic for a college student.
- Use clear headings and bullet points.
"""

    # ----------------------------------------------
    # GEMINI 3.8 FLASH
    # ----------------------------------------------

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return interaction.output_text