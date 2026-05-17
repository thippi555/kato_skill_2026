import json
import os

import boto3
from dotenv import load_dotenv


load_dotenv()


class BedrockClient:

    def __init__(self):
        region = os.getenv("AWS_REGION", "ap-northeast-1")
        self.model_id = os.getenv(
            "BEDROCK_MODEL_ID",
            "jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
        )
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region,
        )

    def analyze_text(self, prompt: str) -> str:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                }
            ],
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response["body"].read())
        content = response_body.get("content", [])

        if not content:
            return ""

        return content[0].get("text", "")
