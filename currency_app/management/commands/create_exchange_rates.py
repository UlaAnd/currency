from typing import Any

from django.core.management.base import BaseCommand

from currency_app.controllers import CurrencyController


class Command(BaseCommand):
    help = "Import rates for last 90 days"

    def handle(self, *args: Any, **options: Any) -> None:
        controller = CurrencyController()
        controller.fetching_currency_data()
