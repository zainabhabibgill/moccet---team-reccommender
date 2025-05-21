import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

team_df = pd.read_csv("Team_1.csv")
project_df = pd.read_csv("Project_1.csv")

# (removing from dataframe)
project_df = project_df[project_df["project_name"] != "AI Chatbot"].reset_index(drop=True)

st.title("Team Recommender Dashboard")
 
# letting user choose a project from the dropdown
project_name = st.selectbox("Select a project", project_df["project_name"])

selected_project = project_df[project_df["project_name"] == project_name].iloc[0]
required_skills = eval(selected_project["required_skills"])

# showing project requirements to the user
st.subheader("Project Requirements")
st.write(f"**Skills Needed:** {', '.join(required_skills)}")
st.write(f"**Deadline (Days):** {selected_project['deadline_days']}")
st.write(f"**Complexity:** {selected_project['complexity_level']}")

# function to score how well a team member matches the required skills
def score_team_member(skills, required):
    return len(set(skills).intersection(set(required)))

team_df_temp = team_df.copy()
team_df_temp["match_score"] = team_df_temp["skills"].apply(eval).apply(
    lambda x: score_team_member(x, required_skills)
)

recommended = team_df_temp.sort_values(by="match_score", ascending=False).head(4)

# creating 2 tabs in the streamlit interface
tab1, tab2 = st.tabs(["👥 Recommended Team", "📖 How It Works"])

with tab1:
    st.subheader("👥 Recommended Team")
    st.dataframe(recommended[["name", "skills", "experience_years", "availability_hours", "match_score"]])
    
    avg_exp = recommended["experience_years"].mean()
    predicted_time = max(10, selected_project["deadline_days"] - int(avg_exp * 1.5))
    st.metric("⏱️ Predicted Completion Time", f"{predicted_time} days")

    # visualising using bar chart
    st.subheader("📊 Skill Match Breakdown")
    fig, ax = plt.subplots()
    ax.bar(recommended["name"], recommended["match_score"], color="skyblue")
    ax.set_ylabel("Match Score")
    ax.set_title("How Well Each Member Matches the Project Skills")
    st.pyplot(fig)

    # visualising using pie chart
    st.subheader("🧩 Skill Coverage")
    covered_skills = set()
    for skills in recommended["skills"].apply(eval):
        covered_skills.update(skills)

    matched = len(set(required_skills).intersection(covered_skills))
    missing = len(set(required_skills)) - matched

    fig2, ax2 = plt.subplots()
    ax2.pie([matched, missing], labels=["Covered", "Missing"], autopct="%1.1f%%", startangle=90, colors=["green", "lightgray"])
    ax2.axis("equal")
    st.pyplot(fig2)

with tab2:
    # providing an explanation of how my reccommendation engine works
    st.subheader("🔍 How the Recommendation Engine Works")
    st.markdown("""
    This app recommends teams based on how well their skills match the project's needs.

    **Here's how it works:**

    - ✅ **Skill Matching**: Each team member is scored based on how many of the required skills they have.
    - 🔢 **Match Score**: We use a simple count of overlapping skills to rank members.
    - 👥 **Top Picks**: The top 4 scorers are recommended for the team.
    - ⏱ **Time Forecast**: The average experience across the recommended team is used to adjust the project duration estimate.

    This is a lightweight model designed for clarity and speed. In future iterations, we could incorporate:
    - Real project history data
    - LSTM-based sequence models for forecasting
    - More complex optimization around availability and team balance
    """)
