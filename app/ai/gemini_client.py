try:
    from google import genai
except ImportError:
    genai = None


from ..config import settings


_client = None


def get_client():

    global _client

    if not settings.gemini_api_key:
        return None

    if genai is None:
        return None

    if _client is None:

        _client = genai.Client(
            api_key=settings.gemini_api_key
        )

    return _client


def generate_text(
    prompt: str,
    model: str,
    system_instruction: str = ""
) -> str:

    client = get_client()

    if client is None:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    config = {
        "temperature": 0.6,
        "max_output_tokens": 3000
    }

    if system_instruction:

        config["system_instruction"] = system_instruction

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()