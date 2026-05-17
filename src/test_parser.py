from skill_parser import SkillParser


def main():

    repository_url = (
        "https://github.com/thippi555/kato_skill_2026.git"
    )

    parser = SkillParser()

    result = parser.analyze_repository(
        repository_url
    )

    print(result)


if __name__ == "__main__":
    main()