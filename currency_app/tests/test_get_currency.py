import pytest

from currency_app.controllers import CurrencyController
from currency_app.models import ExchangeRate


@pytest.mark.django_db(True)
class TestCurrency:
    def test_get_currency(self):
        command = CurrencyController()
        command.fetching_currency_data()
        objects = ExchangeRate.objects.all()
        last = ExchangeRate.objects.last()
        assert objects.count() is not None
        assert last.chf_to_usd is not None
