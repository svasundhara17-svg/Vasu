from .gemini_client import get_client
from .gemini_client import generate_text

from ..config import settings


SYSTEM = """
You are FitBuddy, an educational wellness assistant.

Create safe, practical and general fitness guidance.

Do not diagnose illness.

Do not prescribe medical treatment.

Do not encourage dangerous training.

Do not encourage starvation, dehydration,
extreme dieting or rapid weight change.

For users under 18, do not provide calorie
targets or weight-loss prescriptions.

For younger users, emphasize enjoyable movement,
adequate food, sleep, hydration, good technique
and adult/professional guidance when needed.

Keep the workout achievable.

Include rest and recovery.

Return a plain-text seven-day workout plan.
"""


def _demo(
    name: str,
    goal: str,
    intensity: str
) -> str:

    return f"""
7-Day FitBuddy Demo Plan for {name}

Goal: {goal.title()}
Intensity: {intensity.title()}


DAY 1 - FULL BODY

Warm-up:
5-10 minutes of easy movement.

Main workout:
- Bodyweight squats - 2 to 3 sets
- Incline push-ups - 2 to 3 sets
- Glute bridges - 2 to 3 sets
- Easy walking - 10 minutes

Cooldown:
5 minutes gentle mobility.


DAY 2 - CARDIO AND MOBILITY

Warm-up:
5 minutes easy movement.

Main workout:
- Brisk walking or easy cycling - 20 to 30 minutes
- Gentle mobility - 10 minutes

Cooldown:
Relaxed breathing and stretching.


DAY 3 - LOWER BODY

Warm-up:
5-10 minutes.

Main workout:
- Squat variation - 2 to 3 sets
- Reverse lunges - 2 sets
- Calf raises - 2 to 3 sets
- Glute bridges - 2 to 3 sets

Cooldown:
5-10 minutes easy mobility.


DAY 4 - RECOVERY

Easy walking, light stretching or
beginner-friendly mobility for 20-30 minutes.

Focus on recovery and rest.


DAY 5 - UPPER BODY AND CORE

Warm-up:
5-10 minutes.

Main workout:
- Incline push-ups - 2 to 3 sets
- Resistance-row variation - 2 to 3 sets
- Dead bug - 2 sets
- Short plank holds - 2 sets

Cooldown:
5 minutes.


DAY 6 - CARDIO

Warm-up:
5 minutes.

Main workout:
Comfortable cardio for 20-35 minutes.

Keep the effort controlled.

Cooldown:
5-10 minutes.


DAY 7 - REST AND RECOVERY

Rest.

Gentle walking if desired.

Stay hydrated.

Eat regular balanced meals.

Get adequate sleep.


Safety:
Use comfortable effort.

Stop if you feel pain, dizziness,
or become unwell.

This demo plan is not medical advice.
"""


def generate_workout_gemini(
    user: dict
) -> str:

    if get_client() is None:

        return _demo(
            user["name"],
            user["goal"],
            user["intensity"]
        )

    if user["age"] < 18:

        age_note = """
The user is under 18.

Do not prescribe weight-loss methods,
calorie restriction or body-composition targets.

Focus on general wellness, enjoyable movement,
healthy meals, hydration, sleep and recovery.
"""

    else:

        age_note = """
The user is an adult.

Keep weight-related guidance general.
Do not provide extreme diet or calorie prescriptions.
"""

    prompt = f"""
Create a personalized 7-day workout plan.

USER INFORMATION

Name:
{user['name']}

Age:
{user['age']}

Weight:
{user['weight']} kg

Fitness goal:
{user['goal']}

Workout intensity:
{user['intensity']}

Experience level:
{user['experience_level']}


{age_note}


For each of Day 1 through Day 7 provide:

1. Focus
2. Warm-up
3. Main workout
4. Exercise details
5. Sets/repetitions or duration
6. Rest
7. Cool-down or recovery

Include at least one recovery/rest day.

Keep the plan realistic for the
experience level.

Do not diagnose medical conditions.

Do not include dangerous challenges.

Do not recommend extreme exercise.
"""

    return generate_text(
        prompt,
        settings.gemini_workout_model,
        SYSTEM
    )