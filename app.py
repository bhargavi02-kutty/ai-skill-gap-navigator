import streamlit as st
import pandas as pd

from skill_data import ROLE_SKILLS
from gap_analyzer import calculate_skill_gap
from roadmap import generate_roadmap
from ai_advisor import generate_ai_advice


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
    "for your target job role, and get AI-powered career guidance."
)


# --------------------------------------------------
# SIDEBAR - STUDENT PROFILE
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
            value=0,
            key=f"skill_{skill}"
        )

        student_skills[skill] = level


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button(
    "🔍 Analyze Skill Gap",
    use_container_width=True
):

    if not name.strip():

        st.warning("Please enter your name.")

    else:

        # --------------------------------------------------
        # CALCULATE SKILL GAP
        # --------------------------------------------------

        gap_results = calculate_skill_gap(
            student_skills,
            target_skills
        )

        df = pd.DataFrame(gap_results)


        # --------------------------------------------------
        # SAVE RESULTS IN SESSION STATE
        # --------------------------------------------------

        st.session_state["gap_results"] = gap_results
        st.session_state["student_name"] = name
        st.session_state["branch"] = branch
        st.session_state["year"] = year
        st.session_state["target_role"] = target_role


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "gap_results" in st.session_state:

    gap_results = st.session_state["gap_results"]
    name = st.session_state["student_name"]
    branch = st.session_state["branch"]
    year = st.session_state["year"]
    target_role = st.session_state["target_role"]

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

    top_gaps = (
        df[df["Gap"] > 0]
        .sort_values(
            by=["Importance", "Gap"],
            ascending=False
        )
        .head(5)
    )


    if top_gaps.empty:

        st.success(
            "🎉 You already have all the required skills!"
        )

    else:

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
                min(float(row["Gap"]) / 10, 1.0)
            )


    # --------------------------------------------------
    # RULE-BASED ROADMAP
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
    # RECOMMENDED LEARNING ORDER
    # --------------------------------------------------

    if roadmap:

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


    # --------------------------------------------------
    # GEMINI AI CAREER ADVISOR
    # --------------------------------------------------

    st.header("🤖 AI Career Advisor")

    st.write(
        "Get personalized career guidance using Gemini "
        "based on your skill-gap analysis."
    )


    if st.button(
        "✨ Generate AI Career Advice",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 Gemini is analyzing your profile..."
        ):

            try:

                ai_advice = generate_ai_advice(
                    name=name,
                    branch=branch,
                    year=year,
                    target_role=target_role,
                    gap_results=gap_results
                )

                st.markdown(
                    ai_advice
                )

            except Exception as e:

                st.error(
                    f"Gemini Error: {e}"
                )