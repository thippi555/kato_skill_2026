from github_client import GitHubClient
from file_loader import FileLoader


def main():

    repository_url = (
        "https://github.com/thippi555/kato_skill_2026.git"
    )

    client = GitHubClient()
    loader = FileLoader()

    print("=== Repository Info ===")

    repository_info = client.get_repository_info(
        repository_url
    )

    print(repository_info)

    print("\n=== PDF Files ===")

    pdf_files = client.find_pdf_files(
        repository_url
    )

    print(f"PDF Count: {len(pdf_files)}")

    for pdf_file in pdf_files:

        print(pdf_file)

        pdf_binary = client.download_file(
            pdf_file["download_url"]
        )

        print(
            f"Downloaded Size: {len(pdf_binary)} bytes"
        )

        print("\n=== PDF Text Preview ===")

        pdf_text = loader.load_pdf_text_from_bytes(
            pdf_binary
        )

        print(pdf_text[:3000])


if __name__ == "__main__":
    main()