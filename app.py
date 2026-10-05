import streamlit as st
import pandas as pd

from skill_data import ROLE_SKILLS
from gap_analyzer import calculate_skill_gap
from roadmap import generate_roadmap


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Skill Gap Navigator",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🤖 AI Skill Gap Navigator")

st.write(
    "Analyze your current skills, identify missing skills "
    "for your target job role, and generate a personalized "
    "learning roadmap."
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("🎓 Student Profile")

name = st.sidebar.text_input(
    "Student Name",
    placeholder="Enter your name"
)

branch = st.sidebar.selectbox(
    "BTech Branch",
    [
        "CSE",
        "AI & ML",
        "Data Science",
        "ECE",
        "EEE",
        "Mechanical",
        "Civil",
        "Other"
    ]
)

year = st.sidebar.selectbox(
    "Current Year",
    [
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year"
    ]
)


# --------------------------------------------------
# TARGET ROLE
# --------------------------------------------------

st.header("🎯 Target Job Role")

target_role = st.selectbox(
    "Select your target role",
    list(ROLE_SKILLS.keys())
)


target_skills = ROLE_SKILLS[target_role]


# --------------------------------------------------
# CURRENT SKILLS
# --------------------------------------------------

st.header("💻 Your Current Skills")

st.write(
    "Rate your current knowledge from 0 to 10."
)

student_skills = {}

cols = st.columns(3)

for index, skill in enumerate(target_skills.keys()):

    with cols[index % 3]:

        level = st.slider(
            skill,
            min_value=0,
            max_value=10,
            value=0
        )

        student_skills[skill] = level


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button(
    "🔍 Analyze Skill Gap",
    use_container_width=True
):

    if not name:
        st.warning("Please enter your name.")

    else:

        # Calculate gap
        gap_results = calculate_skill_gap(
            student_skills,
            target_skills
        )

        # Convert to DataFrame
        df = pd.DataFrame(gap_results)


        # --------------------------------------------------
        # STUDENT INFORMATION
        # --------------------------------------------------

        st.success(
            f"Hello {name}! Here is your skill-gap analysis "
            f"for the {target_role} role."
        )

        st.write(
            f"**Branch:** {branch}  \n"
            f"**Year:** {year}  \n"
            f"**Target Role:** {target_role}"
        )


        # --------------------------------------------------
        # SUMMARY
        # --------------------------------------------------

        st.header("📊 Skill Gap Summary")

        total_skills = len(df)

        strong_skills = len(
            df[df["Status"] == "Strong"]
        )

        major_gaps = len(
            df[df["Status"] == "Major Gap"]
        )

        moderate_gaps = len(
            df[df["Status"] == "Moderate Gap"]
        )


        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Skills",
            total_skills
        )

        col2.metric(
            "Strong Skills",
            strong_skills
        )

        col3.metric(
            "Moderate Gaps",
            moderate_gaps
        )

        col4.metric(
            "Major Gaps",
            major_gaps
        )


        # --------------------------------------------------
        # SKILL GAP TABLE
        # --------------------------------------------------

        st.header("📋 Detailed Skill Gap")

        st.dataframe(
            df,
            use_container_width=True
        )


        # --------------------------------------------------
        # TOP SKILLS TO LEARN
        # --------------------------------------------------

        st.header("🔥 Most Important Skills to Learn")

        top_gaps = df[df["Gap"] > 0].head(5)

        for _, row in top_gaps.iterrows():

            st.write(
                f"### {row['Skill']}"
            )

            st.write(
                f"Importance: **{row['Importance']}/10**"
            )

            st.write(
                f"Your Level: **{row['Current Level']}/10**"
            )

            st.write(
                f"Skill Gap: **{row['Gap']}**"
            )

            st.progress(
                min(row["Gap"] / 10, 1.0)
            )


        # --------------------------------------------------
        # ROADMAP
        # --------------------------------------------------

        st.header("🗺️ Personalized Learning Roadmap")

        roadmap = generate_roadmap(
            gap_results
        )

        roadmap_df = pd.DataFrame(
            roadmap
        )

        if not roadmap_df.empty:

            st.dataframe(
                roadmap_df,
                use_container_width=True
            )

        else:

            st.success(
                "🎉 You already have all the required skills!"
            )


        # --------------------------------------------------
        # RECOMMENDED ORDER
        # --------------------------------------------------

        st.header("📚 Recommended Learning Order")

        for index, item in enumerate(
            roadmap,
            start=1
        ):

            st.write(
                f"**Step {index}: {item['Skill']}**"
            )

            st.write(
                f"Level: {item['Level']} | "
                f"Estimated Duration: {item['Duration']}"
            )

            st.divider()