from datetime import datetime
import logging
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db

from .models import User
from .models import Plan

from .schemas import UserInput
from .schemas import FeedbackRequest
from .schemas import PlanResponse

from .ai.gemini_generator import generate_workout_gemini
from .ai.gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)
from .ai.updated_plan import update_workout_plan


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


def _get_user(
    db: Session,
    user_id: str
):

    return db.scalar(
        select(User)
        .where(User.user_id == user_id)
    )


def _get_plan(
    db: Session,
    user_id: str
):

    return db.scalar(
        select(Plan)
        .where(Plan.user_id == user_id)
        .order_by(Plan.id.desc())
    )


def _check_admin(
    key: str | None
):

    if not key or key != settings.admin_key:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin key."
        )


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(

    request: Request,

    user_id: str = Form(...),

    name: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    experience_level: str = Form(
        "beginner"
    ),

    db: Session = Depends(get_db)

):

    data = UserInput(

        user_id=user_id,

        name=name,

        age=age,

        weight=weight,

        goal=goal,

        intensity=intensity,

        experience_level=experience_level

    ).model_dump()


    try:

        workout = generate_workout_gemini(
            data
        )

        tip = generate_nutrition_tip_with_flash(
            data
        )

    except Exception as exc:
        logging.exception("Workout gernerator error")

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "message":
                    f"AI generation failed: {exc}"
            },

            status_code=500
        )


    user = _get_user(
        db,
        data["user_id"]
    )


    if user is None:

        user = User(
            **data
        )

        db.add(user)

    else:

        for key, value in data.items():

            setattr(
                user,
                key,
                value
            )


    plan = _get_plan(
        db,
        data["user_id"]
    )


    if plan is None:

        plan = Plan(

            user_id=data["user_id"],

            original_plan=workout,

            nutrition_tip=tip

        )

        db.add(plan)

    else:

        plan.original_plan = workout

        plan.nutrition_tip = tip

        plan.updated_plan = None

        plan.feedback = None

        plan.updated_at = None


    db.commit()


    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={
            "user": user,
            "plan": plan,
            "message": None
        }
    )


@router.get(
    "/result/{user_id}",
    response_class=HTMLResponse
)
def result(

    request: Request,

    user_id: str,

    db: Session = Depends(get_db)

):

    user = _get_user(
        db,
        user_id
    )

    plan = _get_plan(
        db,
        user_id
    )


    if not user or not plan:

        raise HTTPException(
            status_code=404,
            detail="User or plan not found."
        )


    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={
            "user": user,
            "plan": plan,
            "message": None
        }
    )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    
    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)

):

    data = FeedbackRequest(

        user_id=user_id,

        feedback=feedback

    ).model_dump()


    user = _get_user(
        db,
        data["user_id"]
    )

    plan = _get_plan(
        db,
        data["user_id"]
    )


    if not user or not plan:

        raise HTTPException(
            status_code=404,
            detail="User or plan not found."
        )


    user_data = {

        "name": user.name,

        "age": user.age,

        "weight": user.weight,

        "goal": user.goal,

        "intensity": user.intensity,

        "experience_level":
            user.experience_level

    }


    base_plan = (
        plan.updated_plan
        or plan.original_plan
    )


    try:

        revised = update_workout_plan(

            user_data,

            base_plan,

            data["feedback"]

        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "message":
                    f"Plan update failed: {exc}"
            },

            status_code=502
        )


    plan.updated_plan = revised

    plan.feedback = data["feedback"]

    plan.updated_at = datetime.utcnow()


    db.commit()


    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "user": user,

            "plan": plan,

            "message":
                "Your plan was updated successfully."

        }
    )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    key: str | None = None,

    db: Session = Depends(get_db)

):

    _check_admin(key)


    users = db.scalars(

        select(User)
        .order_by(User.created_at.desc())

    ).all()


    rows = []


    for user in users:

        rows.append({

            "user": user,

            "plan":
                _get_plan(
                    db,
                    user.user_id
                )

        })


    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={
            "rows": rows
        }
    )


@router.get("/api/health")
def health():

    return {

        "status": "ok",

        "service": "FitBuddy"

    }


@router.get(
    "/api/users/{user_id}",
    response_model=PlanResponse
)
def api_get_user(

    user_id: str,

    db: Session = Depends(get_db)

):

    user = _get_user(
        db,
        user_id
    )

    plan = _get_plan(
        db,
        user_id
    )


    if not user or not plan:

        raise HTTPException(
            status_code=404,
            detail="User or plan not found."
        )


    return PlanResponse(

        user_id=user.user_id,

        workout_plan=
            plan.original_plan,

        nutrition_tip=
            plan.nutrition_tip,

        updated_plan=
            plan.updated_plan

    )


@router.delete(
    "/api/users/{user_id}"
)
def api_delete_user(

    user_id: str,

    key: str | None = None,

    db: Session = Depends(get_db)

):

    _check_admin(key)


    user = _get_user(
        db,
        user_id
    )


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )


    plans = db.scalars(

        select(Plan)
        .where(
            Plan.user_id == user_id
        )

    ).all()


    for plan in plans:

        db.delete(plan)


    db.delete(user)

    db.commit()


    return {

        "message": "User deleted",

        "user_id": user_id

    }