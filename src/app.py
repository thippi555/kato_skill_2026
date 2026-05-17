import json

import streamlit as st

from skill_parser import SkillParser


def main():

    st.set_page_config(
        page_title="Skill Sheet AI Analyzer",
        page_icon="📊",
        layout="wide",
    )

    st.title("Skill Sheet AI Analyzer")

    st.caption(
        "GitHub Repository をAIで分析し、"
        "スキル・経験・強みを可視化するツール"
    )

    st.header("Repository Input")

    repository_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/example/project"
    )

    if st.button("Analyze Repository"):

        if not repository_url:
            st.warning("Repository URL を入力してください。")
            return

        with st.spinner("Analyzing repository..."):

            try:

                parser = SkillParser()

                result = parser.analyze_repository(
                    repository_url
                )

                result_json = json.loads(result)

                st.success("Analysis completed.")

                st.header("Analysis Result")

                st.subheader("Profile Summary")

                st.write(
                    result_json.get(
                        "profile_summary",
                        ""
                    )
                )

                st.subheader("Technical Categories")

                st.json(
                    result_json.get(
                        "technical_categories",
                        []
                    )
                )

                st.subheader("Strengths")

                st.json(
                    result_json.get(
                        "strengths",
                        []
                    )
                )

                st.subheader("Interview Points")

                st.json(
                    result_json.get(
                        "interview_points",
                        []
                    )
                )

                st.subheader("Recommended Questions")

                st.json(
                    result_json.get(
                        "recommended_questions",
                        []
                    )
                )

                st.subheader("Full JSON")

                st.json(result_json)

            except Exception as error:

                st.error(f"Error: {error}")


if __name__ == "__main__":
    main()