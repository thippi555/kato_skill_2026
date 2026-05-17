import json
from pathlib import Path

from bedrock_client import BedrockClient
from file_loader import FileLoader
from github_client import GitHubClient


class SkillParser:

    def __init__(self):

        self.github_client = GitHubClient()
        self.bedrock_client = BedrockClient()
        self.file_loader = FileLoader()

    def load_prompt(self):

        project_root = Path(__file__).resolve().parents[1]
        prompt_path = project_root / "prompts" / "skill_analysis_prompt.md"

        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    def clean_json_text(self, text: str):

        cleaned_text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        json_start = cleaned_text.find("{")
        json_end = cleaned_text.rfind("}")

        if json_start != -1 and json_end != -1:
            return cleaned_text[json_start:json_end + 1]

        return cleaned_text

    def load_repository_pdf_text(self, repository_url: str):

        pdf_text = ""

        pdf_files = self.github_client.find_pdf_files(
            repository_url
        )

        for pdf_file in pdf_files:

            pdf_binary = self.github_client.download_file(
                pdf_file["download_url"]
            )

            extracted_text = self.file_loader.load_pdf_text_from_bytes(
                pdf_binary
            )

            pdf_text += f"\n# PDF File: {pdf_file['path']}\n"
            pdf_text += extracted_text
            pdf_text += "\n"

        return pdf_text

    def analyze_repository(self, repository_url: str):

        repository_info = self.github_client.get_repository_info(
            repository_url
        )

        try:
            readme = self.github_client.get_readme(
                repository_url
            )
        except Exception:
            readme = ""

        pdf_text = self.load_repository_pdf_text(
            repository_url
        )

        prompt = self.load_prompt()

        analysis_input = f"""
{prompt}

# Repository Information

{json.dumps(repository_info, ensure_ascii=False, indent=2)}

# README

{readme}

# Skill Sheet PDF Text

{pdf_text}
"""

        result = self.bedrock_client.analyze_text(
            analysis_input
        )

        return self.clean_json_text(result)
