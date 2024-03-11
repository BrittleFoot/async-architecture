from unittest import mock

import pytest
from tracker.models import Task, TaskStatus
from tracker.services import TaskV2Service
from users.models import User, UserRole

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def role(mixer) -> UserRole:
    return mixer.blend(UserRole, name="performer")


@pytest.fixture
def user(mixer, role) -> User:
    return mixer.blend(User, roles=[role])


@pytest.fixture
def task(mixer, user) -> Task:
    return mixer.blend(Task, parformer=user)


@pytest.fixture
def task_service() -> TaskV2Service:
    ts = TaskV2Service()
    ts.producer = mock.MagicMock()
    return ts


def test_create_task(task_service, user):
    task = task_service.create_task("[POPUG-1]", "Test task")

    assert task.summary == "Test task"
    assert task.task_id == "[POPUG-1]"
    assert task.performer == user
    assert task.status == TaskStatus.NEW


def test_reassign_tasks(mixer, task_service, role):
    n = 10
    users = mixer.cycle(n).blend(User, roles=[role])
    unlucky_user = users[0]
    tasks = mixer.cycle(n).blend(Task, performer=unlucky_user, task_id="[POPUG-1]")

    assert unlucky_user.tasks.count() == n

    # Start with all tasks assigned to the first user
    # 10 tasks and users to ensure random test stable

    done_task = tasks[0]
    task_service.complete_task(done_task)

    task_service.reassign_tasks()

    done_task.refresh_from_db()
    assert unlucky_user.tasks.count() < n
    assert done_task.performer == unlucky_user
