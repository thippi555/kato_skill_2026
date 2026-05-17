import streamlit as st


def main():
    st.set_page_config(
        page_title="Skill Sheet AI Analyzer",
        page_icon="📊",
        layout="wide",
    )

    st.title("Skill Sheet AI Analyzer")
    st.caption("スキルシートとGitHub情報をもとに、職務経験をAIで分析・可視化するツール")

    st.header("1. 分析対象入力")

    repository_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/example/skill-sheet-ai-analyzer",
    )

    skill_sheet_text = st.text_area(
        "スキルシート内容",
        placeholder="ここにスキルシートや職務経歴の内容を貼り付けてください。",
        height=250,
    )

    uploaded_file = st.file_uploader(
        "スキルシートファイル",
        type=["txt", "md", "csv"],
    )

    st.header("2. 分析実行")

    if st.button("分析を開始する"):
        if not repository_url and not skill_sheet_text and uploaded_file is None:
            st.warning("GitHub URL、スキルシート内容、またはファイルを指定してください。")
            return

        st.success("分析リクエストを受け付けました。")

        st.subheader("入力内容確認")

        if repository_url:
            st.write("GitHub Repository URL")
            st.code(repository_url)

        if skill_sheet_text:
            st.write("スキルシート入力")
            st.text(skill_sheet_text[:1000])

        if uploaded_file is not None:
            st.write("アップロードファイル")
            st.write(uploaded_file.name)

    st.header("3. 分析結果")

    st.info("現時点では画面骨格のみ。次のステップでGitHub取得処理とBedrock分析処理を接続する。")


if __name__ == "__main__":
    main()