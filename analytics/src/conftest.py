import pytest
from app.test.api_client import AppTestClient
from mixer.backend.django import Mixer
from mixer.backend.django import mixer as _mixer


@pytest.fixture
def api() -> AppTestClient:
    return AppTestClient()


@pytest.fixture
def mixer() -> Mixer:
    return _mixer
