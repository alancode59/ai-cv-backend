import os
from app.prompts.cv_prompt import CV_ANALYSIS_PROMPT
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
import json


class AIServiceError(Exception):
    pass


load_dotenv()

client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

MODEL = os.getenv("CEREBRAS_MODEL", "gpt-oss-120b")


def test_connection():
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "Responde únicamente con la palabra OK"
            }
        ]
    )

    return response.choices[0].message.content


def list_models():
    models = client.models.list()
    return [model.id for model in models.data]


def analyze_cv_with_ai(cv_text: str, job_description: str) -> dict:
    prompt = CV_ANALYSIS_PROMPT.format(
        cv_text=cv_text,
        job_description=job_description
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content
        result = json.loads(content)

        required_keys = [
            "score",
            "skills_detectadas",
            "skills_faltantes",
            "recomendaciones"
        ]

        for key in required_keys:
            if key not in result:
                raise AIServiceError(f"Missing key in AI response: {key}")

        return result

    except json.JSONDecodeError:
        raise AIServiceError("AI returned an invalid JSON response")

    except Exception as error:
        raise AIServiceError(f"AI service error: {str(error)}")
