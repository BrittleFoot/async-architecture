import pytest

from billing.models import Payment
from billing.services import BillingService

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(mixer):
    return mixer.blend("users.User")


@pytest.fixture
def task(mixer, user):
    return mixer.blend("tracker.Task", performer=user, fee=10, reward=100)


@pytest.mark.django_db(transaction=True)
def test_billing(user, task):
    billing_service = BillingService()

    billing_service.charge_fee(task)
    billing_service.pay_reward(task)

    billing_service.end_day()

    payment = Payment.objects.get(user=user)

    assert payment.amount == task.reward - task.fee
