from datetime import datetime

import pytest
from django.test import RequestFactory

from currency_app.controllers import CurrencyController
from currency_app.management.commands.schedule_task import Command
from currency_app.models import ExchangeRate
from currency_app.views import exchange_rate_table


@pytest.mark.django_db(True)
class TestCurrency:
    def test_get_currency_if_no_data(self):
        command = CurrencyController()
        command.fetching_currency_data()
        objects = ExchangeRate.objects.all()
        last = ExchangeRate.objects.last()
        assert objects.count() is not None
        assert last.chf_to_usd is not None

    def test_update_currency_data(self):
        initial_date = datetime(2024, 1, 12)
        instance = ExchangeRate.objects.create(
            date=initial_date.date(),
            eur_to_pln=4.5,
            usd_to_pln=3.8,
            chf_to_pln=4.2,
            eur_to_usd=1.2,
            chf_to_usd=1.1,
        )
        instance.created_at = initial_date
        instance.updated_at = initial_date
        command = Command()
        command.handle()
        objects = ExchangeRate.objects.all()
        last = ExchangeRate.objects.last()
        assert objects.count() is not None
        assert last.date == datetime.now().date()
        assert instance.created_at == initial_date
        assert instance.updated_at == initial_date

    def test_currency_converter(self):
        instance = ExchangeRate.objects.create(
            date=datetime(2024, 1, 17),
            eur_to_pln=4.5,
            usd_to_pln=0,
            chf_to_pln=4.2,
        )
        command = Command()
        command.handle()
        objects = ExchangeRate.objects.all()
        last_obj = ExchangeRate.objects.last()
        assert objects.count() >= 1
        assert instance.chf_to_usd is None
        assert last_obj.chf_to_usd is not None

    @pytest.mark.django_db
    def test_exchange_rate_table_view(self):
        factory = RequestFactory()
        request = factory.get("/selected/")
        response = exchange_rate_table(request)
        assert response.status_code == 200
