import pytest
from rest_framework.test import APIClient

from core.models import CustomUser
from tests import factories


@pytest.fixture
def new_user(db):
    user = CustomUser.objects.create_user(
        username='testuser',
        email='test@mail.ru',
        password='7654321!Ba'
    )
    return user


@pytest.fixture
def auth_client(new_user):
    client = APIClient()
    client.login(username='testuser', password='7654321!Ba')
    return client


@pytest.fixture
def board():
    board = factories.BoardFactory.create()
    return board


@pytest.fixture
def participant(new_user, board):
    factories.ParticipantFactory.create(user=new_user, board=board)


@pytest.fixture
def category(board, new_user, participant):
    category = factories.CategoryFactory.create(board=board, user=new_user)
    return category


@pytest.fixture
def goal(category, new_user):
    goal = factories.GoalFactory.create(category=category, user=new_user)
    return goal


@pytest.fixture
def comment(goal, new_user):
    comment = factories.CommentFactory.create(user=new_user, goal=goal)
    return comment
