from bedrock_client import BedrockClient


def main():

    client = BedrockClient()

    prompt = """
以下を要約してください。

AWS Lambdaを利用したサーバレスアーキテクチャを構築し、
Amazon Bedrockを利用したAI分析システムを開発した。
"""

    result = client.analyze_text(prompt)

    print("=== Bedrock Result ===")
    print(result)


if __name__ == "__main__":
    main()
    