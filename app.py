import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Skill Assessment Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL DASHBOARD STYLING
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main title */
    h1 {
        color: #172554;
        font-weight: 800;
        letter-spacing: -1px;
    }

    /* Section headings */
    h2 {
        color: #1e3a8a;
        font-weight: 700;
    }

    h3 {
        color: #334155;
        font-weight: 650;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #eef2ff;
        border-right: 1px solid #dbeafe;
    }

    section[data-testid="stSidebar"] h2 {
        color: #172554;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #172554;
        font-weight: 800;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    /* Alerts / insight boxes */
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 2rem 0;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("student_skill_assessment.csv")


# ============================================================
# DATA CLEANING
# ============================================================

df["Communication"] = df["Communication"].fillna(
    df["Communication"].mean()
)

df["Leadership"] = df["Leadership"].fillna(
    df["Leadership"].mean()
)

df["Presentation"] = df["Presentation"].fillna(
    df["Presentation"].mean()
)


# ============================================================
# SKILL COLUMNS
# ============================================================

skill_columns = [
    "Python",
    "Problem_Solving",
    "Communication",
    "Teamwork",
    "Leadership",
    "Creativity",
    "Time_Management",
    "Presentation"
]


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🎛️ Dashboard Filters")

selected_department = st.sidebar.multiselect(
    "Select Department",
    options=sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

selected_year = st.sidebar.multiselect(
    "Select Academic Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)


filtered_df = df[
    (df["Department"].isin(selected_department)) &
    (df["Year"].isin(selected_year)) &
    (df["Gender"].isin(selected_gender))
]


st.sidebar.divider()

st.sidebar.metric(
    "Filtered Students",
    filtered_df["Student_ID"].nunique()
)


# ============================================================
# HEADER
# ============================================================

st.title("🎓 Student Skill Assessment Dashboard")

st.markdown(
    """
    ### 📊 Student Performance Intelligence Platform

    Analyze student skills, identify strengths and improvement areas,
    compare departments, and explore individual student performance.
    """
)

st.divider()


# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Students",
        filtered_df["Student_ID"].nunique()
    )

with col2:
    st.metric(
        "📊 Average Score",
        f"{filtered_df['Overall_Score'].mean():.2f}"
    )

with col3:
    st.metric(
        "🌟 Advanced Students",
        (filtered_df["Skill_Level"] == "Advanced").sum()
    )

with col4:
    st.metric(
        "🏆 Top Score",
        f"{filtered_df['Overall_Score'].max():.2f}"
    )


# ============================================================
# DASHBOARD OVERVIEW
# ============================================================

st.divider()

st.subheader("📌 Dashboard Overview")

st.write(
    "Use the filters in the sidebar to dynamically explore "
    "student performance across departments, academic years "
    "and gender."
)


# ============================================================
# SKILL PERFORMANCE ANALYSIS
# ============================================================

st.divider()

st.subheader("📊 Skill Performance Analysis")

skill_averages = (
    filtered_df[skill_columns]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

skill_averages.columns = [
    "Skill",
    "Average Score"
]

fig_skill = px.bar(
    skill_averages,
    x="Skill",
    y="Average Score",
    title="Average Performance Across Skills",
    text_auto=".2f"
)

fig_skill.update_layout(
    yaxis_range=[0, 100],
    xaxis_title="Skill",
    yaxis_title="Average Score",
    height=450
)

st.plotly_chart(
    fig_skill,
    width="stretch"
)


# ============================================================
# SKILL LEVEL DISTRIBUTION
# ============================================================

st.subheader("🎯 Skill Level Distribution")

level_counts = (
    filtered_df["Skill_Level"]
    .value_counts()
    .reset_index()
)

level_counts.columns = [
    "Skill Level",
    "Students"
]

fig_level = px.pie(
    level_counts,
    names="Skill Level",
    values="Students",
    title="Student Proficiency Distribution",
    hole=0.45
)

st.plotly_chart(
    fig_level,
    width="stretch"
)


# ============================================================
# DEPARTMENT PERFORMANCE
# ============================================================

st.divider()

st.subheader("🏢 Department Performance")

department_scores = (
    filtered_df
    .groupby("Department")["Overall_Score"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig_department = px.bar(
    department_scores,
    x="Department",
    y="Overall_Score",
    title="Average Overall Score by Department",
    text_auto=".2f"
)

fig_department.update_layout(
    yaxis_range=[0, 100],
    xaxis_title="Department",
    yaxis_title="Average Overall Score",
    height=450
)

st.plotly_chart(
    fig_department,
    width="stretch"
)


# ============================================================
# PERFORMANCE BY ACADEMIC YEAR
# ============================================================

st.divider()

st.subheader("📚 Performance by Academic Year")

year_scores = (
    filtered_df
    .groupby("Year")["Overall_Score"]
    .mean()
    .reset_index()
)

fig_year = px.line(
    year_scores,
    x="Year",
    y="Overall_Score",
    markers=True,
    text="Overall_Score",
    title="Average Score by Academic Year"
)

fig_year.update_traces(
    texttemplate="%{text:.2f}",
    textposition="top center"
)

fig_year.update_layout(
    yaxis_range=[0, 100],
    xaxis_title="Academic Year",
    yaxis_title="Average Overall Score",
    height=400
)

st.plotly_chart(
    fig_year,
    width="stretch"
)


# ============================================================
# PERFORMANCE BY GENDER
# ============================================================

st.subheader("👥 Performance by Gender")

gender_scores = (
    filtered_df
    .groupby("Gender")["Overall_Score"]
    .mean()
    .reset_index()
)

fig_gender = px.bar(
    gender_scores,
    x="Gender",
    y="Overall_Score",
    text_auto=".2f",
    title="Average Score by Gender"
)

fig_gender.update_layout(
    yaxis_range=[0, 100],
    xaxis_title="Gender",
    yaxis_title="Average Overall Score",
    height=400
)

st.plotly_chart(
    fig_gender,
    width="stretch"
)


# ============================================================
# STUDENT PROFILE EXPLORER
# ============================================================

st.divider()

st.subheader("👤 Student Profile Explorer")

st.write(
    "Select a student to view their individual skill profile, "
    "performance and personalized improvement area."
)

student_names = sorted(
    filtered_df["Student_Name"].unique()
)

if len(student_names) > 0:

    selected_student = st.selectbox(
        "🔎 Select a Student",
        student_names
    )

    student_data = filtered_df[
        filtered_df["Student_Name"] == selected_student
    ].iloc[0]

    info1, info2, info3, info4 = st.columns(4)

    with info1:
        st.metric(
            "Student",
            student_data["Student_Name"]
        )

    with info2:
        st.metric(
            "Department",
            student_data["Department"]
        )

    with info3:
        st.metric(
            "Academic Year",
            f"Year {student_data['Year']}"
        )

    with info4:
        st.metric(
            "Overall Score",
            f"{student_data['Overall_Score']:.2f}"
        )

    profile_col1, profile_col2 = st.columns([1, 2])

    with profile_col1:

        st.markdown("### 🏆 Skill Level")

        skill_level = student_data["Skill_Level"]

        if skill_level == "Advanced":
            st.success("🌟 Advanced")

        elif skill_level == "Intermediate":
            st.warning("📈 Intermediate")

        else:
            st.error("🔰 Beginner")

        st.markdown("### 📊 Performance Summary")

        student_average = student_data[
            skill_columns
        ].mean()

        st.write(
            f"Average skill performance: "
            f"**{student_average:.2f}/100**"
        )

    with profile_col2:

        student_skills = (
            student_data[skill_columns]
            .sort_values(ascending=False)
            .reset_index()
        )

        student_skills.columns = [
            "Skill",
            "Score"
        ]

        fig_student = px.bar(
            student_skills,
            x="Skill",
            y="Score",
            title=f"{selected_student}'s Skill Profile",
            text_auto=".1f"
        )

        fig_student.update_layout(
            yaxis_range=[0, 100],
            xaxis_title="Skill",
            yaxis_title="Score",
            height=450
        )

        st.plotly_chart(
            fig_student,
            width="stretch"
        )

    strongest_skill = student_data[
        skill_columns
    ].idxmax()

    weakest_skill = student_data[
        skill_columns
    ].idxmin()

    strongest_score = student_data[
        strongest_skill
    ]

    weakest_score = student_data[
        weakest_skill
    ]

    strength_col, improvement_col = st.columns(2)

    with strength_col:

        st.markdown("### 💪 Strongest Skill")

        st.success(
            f"**{strongest_skill}** — "
            f"{strongest_score:.1f}/100"
        )

    with improvement_col:

        st.markdown("### 🎯 Improvement Area")

        st.warning(
            f"**{weakest_skill}** — "
            f"{weakest_score:.1f}/100"
        )

    recommendation_map = {
        "Python":
            "Practice coding problems, Python projects and automation tasks.",
        "Problem_Solving":
            "Work on logical reasoning, coding challenges and real-world case studies.",
        "Communication":
            "Practice group discussions, speaking exercises and professional communication.",
        "Teamwork":
            "Participate in collaborative projects and team-based activities.",
        "Leadership":
            "Take responsibility in team projects and practice decision-making.",
        "Creativity":
            "Explore innovative projects, brainstorming and creative problem-solving.",
        "Time_Management":
            "Use structured schedules, prioritization and task-planning techniques.",
        "Presentation":
            "Practice public speaking, presentations and explaining technical concepts."
    }

    recommendation = recommendation_map.get(
        weakest_skill,
        "Focus on consistent practice to improve this skill."
    )

    st.info(
        f"🎯 **Focus on improving {weakest_skill}.** "
        f"{recommendation}"
    )

else:

    st.warning(
        "No students match the selected filters."
    )


# ============================================================
# TOP STUDENTS LEADERBOARD
# ============================================================

st.divider()

st.subheader("🏆 Top Students Leaderboard")

st.write(
    "Explore the highest-performing students based on "
    "their overall skill assessment score."
)

leaderboard = (
    filtered_df[
        [
            "Student_Name",
            "Department",
            "Year",
            "Overall_Score",
            "Skill_Level"
        ]
    ]
    .sort_values(
        "Overall_Score",
        ascending=False
    )
    .head(10)
    .reset_index(drop=True)
)

leaderboard.index = leaderboard.index + 1

leaderboard.insert(
    0,
    "Rank",
    leaderboard.index
)

leaderboard["Year"] = leaderboard[
    "Year"
].apply(
    lambda x: f"Year {x}"
)

leaderboard["Overall_Score"] = leaderboard[
    "Overall_Score"
].round(2)

st.dataframe(
    leaderboard,
    width="stretch",
    hide_index=True
)

if len(leaderboard) > 0:

    top_student = leaderboard.iloc[0]

    st.success(
        f"🥇 **Top Performer:** "
        f"{top_student['Student_Name']} from "
        f"**{top_student['Department']}** with an overall score "
        f"of **{top_student['Overall_Score']:.2f}**."
    )


# ============================================================
# AUTOMATIC PERFORMANCE INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Performance Insights")

st.write(
    "Automatically generated insights based on the "
    "currently selected students."
)

if len(filtered_df) > 0:

    overall_average = filtered_df[
        "Overall_Score"
    ].mean()

    filtered_skill_averages = (
        filtered_df[skill_columns]
        .mean()
        .sort_values(ascending=False)
    )

    strongest_skill = filtered_skill_averages.idxmax()
    weakest_skill = filtered_skill_averages.idxmin()

    strongest_skill_score = filtered_skill_averages.max()
    weakest_skill_score = filtered_skill_averages.min()

    skill_gap = (
        strongest_skill_score -
        weakest_skill_score
    )

    department_performance = (
        filtered_df
        .groupby("Department")["Overall_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    best_department = department_performance.idxmax()
    best_department_score = department_performance.max()

    lowest_department = department_performance.idxmin()
    lowest_department_score = department_performance.min()

    year_performance = (
        filtered_df
        .groupby("Year")["Overall_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    best_year = year_performance.idxmax()
    best_year_score = year_performance.max()

    gender_performance = (
        filtered_df
        .groupby("Gender")["Overall_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    highest_gender = gender_performance.idxmax()
    highest_gender_score = gender_performance.max()

    advanced_count = (
        filtered_df["Skill_Level"] == "Advanced"
    ).sum()

    intermediate_count = (
        filtered_df["Skill_Level"] == "Intermediate"
    ).sum()

    beginner_count = (
        filtered_df["Skill_Level"] == "Beginner"
    ).sum()

    insight1, insight2, insight3 = st.columns(3)

    with insight1:

        st.markdown("### 🏆 Best Department")

        st.success(
            f"**{best_department}**\n\n"
            f"Average Score: **{best_department_score:.2f}**"
        )

    with insight2:

        st.markdown("### 💪 Strongest Skill")

        st.success(
            f"**{strongest_skill}**\n\n"
            f"Average Score: **{strongest_skill_score:.2f}**"
        )

    with insight3:

        st.markdown("### 🎯 Weakest Skill")

        st.warning(
            f"**{weakest_skill}**\n\n"
            f"Average Score: **{weakest_skill_score:.2f}**"
        )

    st.markdown("### 📋 Key Findings")

    st.info(
        f"📊 **Overall Performance:** "
        f"The average overall score is "
        f"**{overall_average:.2f}/100**."
    )

    st.info(
        f"💪 **Skill Strength:** "
        f"**{strongest_skill}** is the strongest skill with "
        f"an average score of **{strongest_skill_score:.2f}**."
    )

    st.warning(
        f"🎯 **Improvement Area:** "
        f"**{weakest_skill}** has the lowest average score at "
        f"**{weakest_skill_score:.2f}**."
    )

    st.info(
        f"📈 **Skill Gap:** "
        f"The difference between the strongest and weakest "
        f"skill is **{skill_gap:.2f} points**."
    )

    st.info(
        f"📚 **Academic Year Insight:** "
        f"**Year {best_year}** has the highest average score "
        f"at **{best_year_score:.2f}**."
    )

    st.info(
        f"👥 **Gender Performance:** "
        f"**{highest_gender}** has the higher average score "
        f"at **{highest_gender_score:.2f}**."
    )

    st.info(
        f"🏢 **Department Gap:** "
        f"**{best_department}** leads with "
        f"**{best_department_score:.2f}**, while "
        f"**{lowest_department}** has the lowest average of "
        f"**{lowest_department_score:.2f}**."
    )

    st.markdown("### 🎯 Skill Level Summary")

    level1, level2, level3 = st.columns(3)

    with level1:
        st.metric(
            "🌟 Advanced",
            advanced_count
        )

    with level2:
        st.metric(
            "📈 Intermediate",
            intermediate_count
        )

    with level3:
        st.metric(
            "🔰 Beginner",
            beginner_count
        )

else:

    st.warning(
        "No data is available for the selected filters."
    )


# ============================================================
# ASSESSMENT TREND ANALYSIS
# ============================================================

st.divider()

st.subheader("📅 Assessment Trend Analysis")

st.write(
    "Track how student performance changes across "
    "the assessment period."
)

if len(filtered_df) > 0:

    trend_df = filtered_df.copy()

    trend_df["Assessment_Date"] = pd.to_datetime(
        trend_df["Assessment_Date"]
    )

    trend_df["Month"] = (
        trend_df["Assessment_Date"]
        .dt.strftime("%b")
    )

    trend_df["Month_Number"] = (
        trend_df["Assessment_Date"]
        .dt.month
    )

    monthly_scores = (
        trend_df
        .groupby(
            ["Month_Number", "Month"]
        )["Overall_Score"]
        .mean()
        .reset_index()
        .sort_values("Month_Number")
    )

    monthly_assessments = (
        trend_df
        .groupby(
            ["Month_Number", "Month"]
        )
        .size()
        .reset_index(
            name="Assessments"
        )
        .sort_values("Month_Number")
    )

    st.markdown(
        "### 📈 Monthly Average Performance"
    )

    fig_monthly = px.line(
        monthly_scores,
        x="Month",
        y="Overall_Score",
        markers=True,
        text="Overall_Score",
        title="Average Overall Score by Assessment Month"
    )

    fig_monthly.update_traces(
        texttemplate="%{text:.2f}",
        textposition="top center"
    )

    fig_monthly.update_layout(
        yaxis_range=[0, 100],
        xaxis_title="Assessment Month",
        yaxis_title="Average Overall Score",
        height=450
    )

    st.plotly_chart(
        fig_monthly,
        width="stretch"
    )

    st.markdown(
        "### 📊 Assessment Volume"
    )

    fig_volume = px.bar(
        monthly_assessments,
        x="Month",
        y="Assessments",
        text_auto=True,
        title="Number of Assessments Conducted Each Month"
    )

    fig_volume.update_layout(
        xaxis_title="Assessment Month",
        yaxis_title="Number of Assessments",
        height=400
    )

    st.plotly_chart(
        fig_volume,
        width="stretch"
    )

    if len(monthly_scores) >= 2:

        first_score = monthly_scores.iloc[0][
            "Overall_Score"
        ]

        last_score = monthly_scores.iloc[-1][
            "Overall_Score"
        ]

        score_change = last_score - first_score

        best_month_row = monthly_scores.loc[
            monthly_scores["Overall_Score"].idxmax()
        ]

        lowest_month_row = monthly_scores.loc[
            monthly_scores["Overall_Score"].idxmin()
        ]

        trend_col1, trend_col2, trend_col3 = st.columns(3)

        with trend_col1:
            st.metric(
                "📈 Best Month",
                best_month_row["Month"],
                f"{best_month_row['Overall_Score']:.2f}"
            )

        with trend_col2:
            st.metric(
                "📉 Lowest Month",
                lowest_month_row["Month"],
                f"{lowest_month_row['Overall_Score']:.2f}"
            )

        with trend_col3:
            st.metric(
                "🔄 Score Change",
                f"{score_change:+.2f}"
            )

        if score_change > 0:

            st.success(
                f"📈 Performance improved by "
                f"**{score_change:.2f} points** from the "
                f"first assessment month to the last."
            )

        elif score_change < 0:

            st.warning(
                f"📉 Performance decreased by "
                f"**{abs(score_change):.2f} points** from the "
                f"first assessment month to the last."
            )

        else:

            st.info(
                "➡️ Overall performance remained stable "
                "across the assessment period."
            )

else:

    st.warning(
        "No assessment data is available for the selected filters."
    )


# ============================================================
# SKILL GAP & IMPROVEMENT ANALYSIS
# ============================================================

st.divider()

st.subheader("🧠 Skill Gap & Improvement Analysis")

st.write(
    "Compare skill performance across departments and identify "
    "the areas that require the most improvement."
)

if len(filtered_df) > 0:

    department_skill_scores = (
        filtered_df
        .groupby("Department")[skill_columns]
        .mean()
        .round(2)
    )

    st.markdown(
        "### 🔥 Department Skill Heatmap"
    )

    fig_heatmap = px.imshow(
        department_skill_scores,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="RdYlGn",
        zmin=0,
        zmax=100,
        title="Average Skill Score by Department"
    )

    fig_heatmap.update_layout(
        xaxis_title="Skills",
        yaxis_title="Department",
        height=550
    )

    st.plotly_chart(
        fig_heatmap,
        width="stretch"
    )

    st.markdown(
        "### 📊 Overall Skill Ranking"
    )

    overall_skill_scores = (
        filtered_df[skill_columns]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    overall_skill_scores.columns = [
        "Skill",
        "Average Score"
    ]

    fig_skill_gap = px.bar(
        overall_skill_scores,
        x="Skill",
        y="Average Score",
        text_auto=".2f",
        title="Skill Strength Ranking"
    )

    fig_skill_gap.update_layout(
        yaxis_range=[0, 100],
        xaxis_title="Skill",
        yaxis_title="Average Score",
        height=450
    )

    st.plotly_chart(
        fig_skill_gap,
        width="stretch"
    )

    strongest_skill = overall_skill_scores.iloc[0]
    weakest_skill = overall_skill_scores.iloc[-1]

    analysis_col1, analysis_col2 = st.columns(2)

    with analysis_col1:

        st.markdown("### 💪 Strongest Skill")

        st.success(
            f"**{strongest_skill['Skill']}**\n\n"
            f"Average Score: "
            f"**{strongest_skill['Average Score']:.2f}/100**"
        )

    with analysis_col2:

        st.markdown("### 🎯 Priority Improvement Area")

        st.warning(
            f"**{weakest_skill['Skill']}**\n\n"
            f"Average Score: "
            f"**{weakest_skill['Average Score']:.2f}/100**"
        )

    st.markdown(
        "### 🏢 Department Improvement Areas"
    )

    department_insights = []

    for department in department_skill_scores.index:

        department_data = (
            department_skill_scores
            .loc[department]
            .sort_values()
        )

        weakest = department_data.index[0]
        weakest_score = department_data.iloc[0]

        strongest = department_data.index[-1]
        strongest_score = department_data.iloc[-1]

        department_insights.append({
            "Department": department,
            "Strongest Skill": strongest,
            "Strongest Score": round(
                strongest_score,
                2
            ),
            "Weakest Skill": weakest,
            "Weakest Score": round(
                weakest_score,
                2
            )
        })

    department_insights_df = pd.DataFrame(
        department_insights
    )

    st.dataframe(
        department_insights_df,
        width="stretch",
        hide_index=True
    )

    st.markdown(
        "### 💡 Improvement Recommendation"
    )

    st.info(
        f"🎯 Based on the selected students, "
        f"**{weakest_skill['Skill']}** is currently the "
        f"lowest-performing skill with an average score of "
        f"**{weakest_skill['Average Score']:.2f}/100**. "
        f"Targeted training, practice activities and practical "
        f"projects can be used to improve this area."
    )

else:

    st.warning(
        "No data is available for the selected filters."
    )
    # ============================================================
# EXPORT & REPORTS
# ============================================================

st.divider()

st.subheader("📥 Export & Reports")

st.write(
    "Download the currently filtered student data and "
    "performance leaderboard for further analysis."
)

# ------------------------------------------------------------
# Prepare filtered data for export
# ------------------------------------------------------------

export_df = filtered_df.copy()

# Convert assessment date to a clean date format
if "Assessment_Date" in export_df.columns:
    export_df["Assessment_Date"] = pd.to_datetime(
        export_df["Assessment_Date"]
    ).dt.strftime("%Y-%m-%d")


# Convert filtered data to CSV
filtered_csv = export_df.to_csv(
    index=False
).encode("utf-8")


# ------------------------------------------------------------
# Prepare leaderboard for export
# ------------------------------------------------------------

export_leaderboard = (
    filtered_df[
        [
            "Student_Name",
            "Department",
            "Year",
            "Gender",
            "Overall_Score",
            "Skill_Level"
        ]
    ]
    .sort_values(
        "Overall_Score",
        ascending=False
    )
    .head(10)
    .reset_index(drop=True)
)

export_leaderboard.insert(
    0,
    "Rank",
    range(1, len(export_leaderboard) + 1)
)

export_leaderboard["Overall_Score"] = (
    export_leaderboard["Overall_Score"].round(2)
)

leaderboard_csv = export_leaderboard.to_csv(
    index=False
).encode("utf-8")


# ------------------------------------------------------------
# Download buttons
# ------------------------------------------------------------

download_col1, download_col2 = st.columns(2)

with download_col1:

    st.markdown("### 📄 Student Data")

    st.download_button(
        label="⬇️ Download Filtered Student Data",
        data=filtered_csv,
        file_name="filtered_student_skill_data.csv",
        mime="text/csv",
        width="stretch"
    )

with download_col2:

    st.markdown("### 🏆 Leaderboard")

    st.download_button(
        label="⬇️ Download Top 10 Leaderboard",
        data=leaderboard_csv,
        file_name="student_leaderboard.csv",
        mime="text/csv",
        width="stretch"
    )


st.success(
    f"✅ Export ready: {filtered_df['Student_ID'].nunique()} "
    "students are included based on the current filters."
)