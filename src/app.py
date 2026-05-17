import json

import pandas as pd
import plotly.express as px
import streamlit as st
from json_repair import repair_json

from skill_parser import SkillParser


def parse_json_safely(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        repaired = repair_json(text)
        return json.loads(repaired)


def show_list(title, values):
    st.subheader(title)

    if not values:
        st.info("データなし")
        return

    for value in values:
        st.write(f"- {value}")


def show_categories(categories):
    st.header("Technical Categories")

    if not categories:
        st.info("技術カテゴリなし")
        return

    dataframe = pd.DataFrame({
        "category": categories,
        "count": [1] * len(categories)
    })

    figure = px.bar(
        dataframe,
        x="category",
        y="count",
        title="Technical Categories"
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


def show_recent_projects(recent_projects):
    st.header("Recent Projects")

    if not recent_projects:
        st.info("直近案件データなし")
        return

    for project in recent_projects:
        title = project.get("project_name", "Project")
        period = project.get("period", "")

        with st.expander(f"{period} {title}", expanded=True):
            st.write(project.get("summary", ""))

            st.write("**Technologies**")
            st.write(project.get("technologies", []))

            st.write("**Cloud**")
            st.write(project.get("cloud", []))

            st.write("**Role**")
            st.write(project.get("role", ""))

            st.write("**Phases**")
            st.write(project.get("phases", []))

            st.write("**Architecture Points**")
            st.write(project.get("architecture_points", []))

            st.write("**Technical Challenges**")
            st.write(project.get("technical_challenges", []))

            st.write("**Improvements**")
            st.write(project.get("improvements", []))

            st.write("**Interview Highlights**")
            st.write(project.get("interview_highlights", []))


def show_cloud_experience(cloud_experience):
    st.header("Cloud Experience")

    if not cloud_experience:
        st.info("クラウド経験データなし")
        return

    providers = []

    for item in cloud_experience:
        if isinstance(item, dict):
            provider = item.get("provider", "Other")
        else:
            provider = str(item)

        providers.append(provider)

    dataframe = pd.DataFrame({
        "provider": providers,
        "count": [1] * len(providers)
    })

    figure = px.bar(
        dataframe,
        x="provider",
        y="count",
        title="Cloud Providers"
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )

    for item in cloud_experience:
        if isinstance(item, dict):
            provider = item.get("provider", "Other")

            with st.expander(provider, expanded=True):
                st.json(item)
        else:
            st.write(f"- {item}")


def show_ai_experience(ai_experience):
    st.header("AI Experience")

    if not ai_experience:
        st.info("AI経験データなし")
        return

    for item in ai_experience:
        if isinstance(item, dict):
            category = item.get("category", "AI")

            with st.expander(category, expanded=True):
                st.json(item)
        else:
            st.write(f"- {item}")


def show_architecture_experience(architecture_experience):
    st.header("Architecture Experience")

    if not architecture_experience:
        st.info("アーキテクチャ経験データなし")
        return

    for item in architecture_experience:
        if isinstance(item, dict):
            category = item.get("category", "Architecture")

            with st.expander(category, expanded=True):
                st.json(item)
        else:
            st.write(f"- {item}")


def show_development_process(development_process):
    st.header("Development Process")

    if not development_process:
        st.info("工程経験データなし")
        return

    for item in development_process:
        if isinstance(item, dict):
            with st.expander("Process", expanded=False):
                st.json(item)
        else:
            st.write(f"- {item}")


def show_metrics(result_json):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Categories", len(result_json.get("technical_categories", [])))

    with col2:
        st.metric("Cloud Providers", len(result_json.get("cloud_experience", [])))

    with col3:
        st.metric("Recent Projects", len(result_json.get("recent_projects", [])))

    with col4:
        st.metric("Interview Questions", len(result_json.get("recommended_questions", [])))


def main():
    st.set_page_config(
        page_title="Skill Sheet AI Analyzer",
        page_icon="📊",
        layout="wide",
    )

    st.title("Skill Sheet AI Analyzer")
    st.caption(
        "GitHub上のスキルシートPDFを取得し、"
        "Amazon Bedrockで職務経験・技術領域・強みを分析するツール"
    )

    st.header("Repository Input")

    repository_url = st.text_input(
        "GitHub Repository URL",
        value="https://github.com/thippi555/kato_skill_2026.git"
    )

    if st.button("Analyze Skill Sheet"):

        if not repository_url:
            st.warning("Repository URL を入力してください。")
            return

        with st.spinner("Analyzing GitHub skill sheet PDF..."):

            try:
                parser = SkillParser()

                result = parser.analyze_repository(repository_url)

                result_json = parse_json_safely(result)

                st.success("Analysis completed.")

                show_metrics(result_json)

                st.header("Profile Summary")
                st.write(result_json.get("profile_summary", ""))

                show_recent_projects(
                    result_json.get("recent_projects", [])
                )

                show_categories(
                    result_json.get("technical_categories", [])
                )

                show_cloud_experience(
                    result_json.get("cloud_experience", [])
                )

                show_ai_experience(
                    result_json.get("ai_experience", [])
                )

                show_development_process(
                    result_json.get("development_process", [])
                )

                show_architecture_experience(
                    result_json.get("architecture_experience", [])
                )

                show_list(
                    "Strengths",
                    result_json.get("strengths", [])
                )

                show_list(
                    "Interview Points",
                    result_json.get("interview_points", [])
                )

                show_list(
                    "Recommended Questions",
                    result_json.get("recommended_questions", [])
                )

                show_list(
                    "Career Direction",
                    result_json.get("career_direction", [])
                )

                st.header("Full JSON")
                st.json(result_json)

            except Exception as error:
                st.error(f"Error: {error}")


if __name__ == "__main__":
    main()