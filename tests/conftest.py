import os
import sys

from pathlib import Path


sys.path.insert(
    0,
    str(
        Path(__file__)
        .resolve()
        .parents[1]
    )
)


os.environ["DATABASE_URL"] = (
    "sqlite:///./test_fitbuddy.db"
)

os.environ["GEMINI_API_KEY"] = ""

os.environ["ADMIN_KEY"] = "test-admin"


from fastapi.testclient import TestClient

import pytest

from app.main import app

from app.database import Base
from app.database import engine


@pytest.fixture()
def client():

    Base.metadata.drop_all(
        bind=engine
    )

    Base.metadata.create_all(
        bind=engine
    )

    with TestClient(app) as client:

        yield client