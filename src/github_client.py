import os

from dotenv import load_dotenv
from github import Github


load_dotenv()


class GitHubClient:

    def __init__(self):

        token = os.getenv("GITHUB_TOKEN")

        if not token:
            raise ValueError("GITHUB_TOKEN is not set.")

        self.github = Github(token)

    def get_repository_name(self, repository_url: str):

        repository_name = (
            repository_url
            .replace("https://github.com/", "")
            .replace(".git", "")
            .strip("/")
        )

        return repository_name

    def get_repository_info(self, repository_url: str):

        repository_name = self.get_repository_name(
            repository_url
        )

        repo = self.github.get_repo(repository_name)

        repository_data = {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "languages": repo.get_languages(),
            "stars": repo.stargazers_count,
            "url": repo.html_url,
        }

        return repository_data

    def get_readme(self, repository_url: str):

        repository_name = self.get_repository_name(
            repository_url
        )

        repo = self.github.get_repo(repository_name)

        readme = repo.get_readme()

        return readme.decoded_content.decode("utf-8")

    def find_pdf_files(self, repository_url: str):

        repository_name = self.get_repository_name(
            repository_url
        )

        repo = self.github.get_repo(repository_name)

        pdf_files = []

        contents = repo.get_contents("")

        while contents:

            file_content = contents.pop(0)

            if file_content.type == "dir":

                contents.extend(
                    repo.get_contents(file_content.path)
                )

            elif file_content.path.lower().endswith(".pdf"):

                pdf_files.append({
                    "name": file_content.name,
                    "path": file_content.path,
                    "download_url": file_content.download_url
                })

        return pdf_files