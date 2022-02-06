from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
from alembic import command


# SQLALCHEMY_DATABASE_URL = f'postgresql://postgre:password@localhost:5432/fastapo_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostaname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    #this fixture returns a fastapi test client needed to send in the API commands.
    def override_get_db():
    
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "guru@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    # print (res.json())
    new_user = res.json()
    # res doesn't return the password. So let's add it
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "guru2@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    # print (res.json())
    new_user = res.json()
    # res doesn't return the password. So let's add it
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
        }, {
            "title": "second title",
        "content": "second content",
        "owner_id": test_user['id']
        }, {
            "title": "third title",
        "content": "third content",
        "owner_id": test_user['id']
        }, {
            "title": "fourth title",
        "content": "fourth content",
        "owner_id": test_user2['id']
        }]

    def create_post_Model(post):
        return models.Post(**post)

    post_map = map(create_post_Model, post_data)
    posts = list(post_map)

    # session.add_all([models.Post(title:"first title", content="first content", owner_id=test_user['id']),
    #                  models.Post(title:"second title", content="second content", owner_id=test_user['id']),
    #                  models.Post(title:"third title", content="third content", owner_id=test_user['id'])])
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    print (posts)
    return posts
    


