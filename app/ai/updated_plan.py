from .gemini_client import get_client
from .gemini_client import generate_text

from ..config import settings

from .gemini_generator import SYSTEM


def update_workout_plan(
    user: dict,
    original_plan: str,
    feedback: str
) -> str:

    if get_client() is None:

        return (
            original_plan
            + "\n\n"
            + "Feedback applied in demo mode: "
            + feedback
            + "\n"
            + "Keep changes gradual and include recovery."
        )

    prompt = f"""
Revise the existing 7-day workout plan
using the user's feedback.

USER PROFILE

Age:
{user['age']}

Goal:
{user['goal']}

Intensity:
{user['intensity']}

Experience:
{user['experience_level']}


ORIGINAL PLAN

{original_plan}


USER FEEDBACK

{feedback}


Return a complete revised 7-day plan.

Do not return only a list of changes.

Keep safe progression.

Include recovery and rest.

Keep the same general fitness goal.

Do not prescribe dangerous training.

Do not prescribe extreme diet or exercise behavior.
"""

    return generate_text(
        prompt,
        settings.gemini_workout_model,
        SYSTEM
    )