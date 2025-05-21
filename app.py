import streamlit as st
import pandas as pd
import numpy as np

team_df = pd.read_csv("Team 1.csv")
project_df = pd.read_csv("Project 1.csv")


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

team_df["match_score"] = team_df["skills"].apply(eval).apply(lambda x: score_team_member(x, required_skills))
recommended = team_df.sort_values(by="match_score", ascending=False).head(4)


st.subheader("👥 Recommended Team")
st.dataframe(recommended[["name", "skills", "experience_years", "availability_hours", "match_score"]])


avg_exp = recommended["experience_years"].mean()
predicted_time = max(10, selected_project["deadline_days"] - int(avg_exp * 1.5))
st.metric("⏱️ Predicted Completion Time", f"{predicted_time} days")

st.subheader("📖 How It Works")
st.markdown("""
- Team members are matched based on overlapping skills.
- Higher experience helps reduce project completion time.
- Forecast is a simple function of team experience vs project deadline.
""")
