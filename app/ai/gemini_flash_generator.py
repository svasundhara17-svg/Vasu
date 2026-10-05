from .gemini_client import get_client
from .gemini_client import generate_text

from ..config import settings


SYSTEM = """
You are FitBuddy's nutrition and recovery assistant.

Give one concise general wellness tip.

Do not prescribe restrictive diets.

Do not prescribe supplements.

Do not prescribe fasting.

Do not provide medical treatment.

For minors, never provide calorie targets
or weight-loss instructions.

Encourage regular balanced meals,
hydration, sleep and appropriate recovery.
"""


def _demo(goal: str) -> str:

    tips = {

        "muscle gain":
            "Include a protein-rich food in regular meals, "
            "drink enough water, and allow recovery between "
            "harder sessions.",

        "weight loss":
            "Focus on regular balanced meals, fruits and "
            "vegetables, hydration, enjoyable movement and "
            "consistent sleep rather than extreme restriction.",

        "general wellness":
            "Build meals around a variety of foods, stay "
            "hydrated, and prioritize consistent sleep "
            "and recovery.",

        "flexibility":
            "Stay hydrated and include regular meals plus "
            "gentle mobility work. Recovery and sleep support "
            "your overall wellness."
    }

    return tips.get(
        goal.lower(),
        tips["general wellness"]
    )


def generate_nutrition_tip_with_flash(
    user: dict
) -> str:

    if get_client() is None:

        return _demo(
            user["goal"]
        )

    if user["age"] < 18:

        age_note = """
Do not mention calorie restriction
or weight loss.
"""

    else:

        age_note = ""

    prompt = f"""
Give one practical nutrition or recovery tip.

Fitness goal:
{user['goal']}

Age:
{user['age']}

Workout intensity:
{user['intensity']}

{age_note}

Limit the answer to 2-4 sentences.

Keep it general wellness guidance.
"""

    return generate_text(
        prompt,
        settings.gemini_tip_model,
        SYSTEM
    )