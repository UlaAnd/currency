import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory

from currency_app.controllers import CurrencyController
from currency_app.forms import ColumnVisibilityForm
from currency_app.models import ExchangeRate
from currency_app.views import exchange_rate_table


@pytest.mark.django_db(True)
class TestCurrency:
    def test_get_currency(self):
        command = CurrencyController()
        command.fetching_currency_data()
        objects = ExchangeRate.objects.all()
        last = ExchangeRate.objects.last()
        assert objects.count() is not None
        assert last.chf_to_usd is not None

    @pytest.mark.django_db
    def test_exchange_rate_table_view(self):
        factory = RequestFactory()
        request = factory.get("/selected/")
        response = exchange_rate_table(request)
        assert response.status_code == 200
        post_data = {"eur_to_pln": True}
        request = factory.post("/selected/", post_data)
        request.session = {}
        request.session["invisible_columns"] = []
        ColumnVisibilityForm(data=post_data)
        request._messages = FallbackStorage(request)
        request._messages.__class__ = FallbackStorage
        request._messages._queued_messages = [
            {
                "level": 25,
                "message": "Export selected data to CSV clicked!",
                "extra_tags": "",
            }
        ]
        response = exchange_rate_table(request)
        assert response.status_code == 200
        assert b"Export selected data to CSV clicked!" in response.content
