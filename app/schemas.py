from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class UserInput(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=64
    )

    name: str = Field(
        min_length=1,
        max_length=100
    )

    age: int = Field(
        ge=10,
        le=100
    )

    weight: float = Field(
        gt=20,
        lt=300
    )

    goal: str = Field(
        min_length=2,
        max_length=50
    )

    intensity: str = Field(
        pattern="^(low|medium|high)$"
    )

    experience_level: str = Field(
        default="beginner",
        pattern="^(beginner|intermediate|advanced)$"
    )

    @field_validator("goal")
    @classmethod
    def clean_goal(cls, value: str) -> str:

        return " ".join(
            value.strip().lower().split()
        )

    @field_validator("user_id", "name")
    @classmethod
    def clean_text(cls, value: str) -> str:

        return value.strip()


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=64
    )

    feedback: str = Field(
        min_length=3,
        max_length=1000
    )


class PlanResponse(BaseModel):

    user_id: str

    workout_plan: str

    nutrition_tip: str

    updated_plan: str | None = None