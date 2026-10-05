from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    age: Mapped[int] = mapped_column(
        Integer
    )

    weight: Mapped[float] = mapped_column(
        Float
    )

    goal: Mapped[str] = mapped_column(
        String(50)
    )

    intensity: Mapped[str] = mapped_column(
        String(20)
    )

    experience_level: Mapped[str] = mapped_column(
        String(30),
        default="beginner"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Plan(Base):

    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(64),
        index=True
    )

    original_plan: Mapped[str] = mapped_column(
        Text
    )

    nutrition_tip: Mapped[str] = mapped_column(
        Text
    )

    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )