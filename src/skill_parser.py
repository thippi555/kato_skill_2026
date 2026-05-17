import json
from pathlib import Path

from github_client import GitHubClient
from bedrock_client import BedrockClient


class SkillParser:

    def __init__(self):

        self.github_client = GitHubClient()
        self.bedrock_client = BedrockClient()

    def load_prompt(self):

        project_root = Path(__file__).resolve().parents[1]
        prompt_path = project_root / "prompts" / "skill_analysis_prompt.md"

        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    def analyze_repository(self, repository_url: str):

        repository_info = self.github_client.get_repository_info(
            repository_url
        )

        readme = self.github_client.get_readme(
            repository_url
        )

        prompt = self.load_prompt()

        analysis_input = f"""
{prompt}

# Repository Information

{json.dumps(repository_info, ensure_ascii=False, indent=2)}

# README

{readme}
"""

        result = self.bedrock_client.analyze_text(
            analysis_input
        )

        return result
