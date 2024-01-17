from typing import Any

from django.core.management.base import BaseCommand
from django_tables2.export import TableExport

from currency_app.controllers import CurrencyController
from currency_app.models import ExchangeRate
from currency_app.tables import ExchangeRateTable


class Command(BaseCommand):
    help = "Import rates for last 90 days"

    def handle(self, *args: Any, **options: Any) -> None:
        controller = CurrencyController()
        controller.fetching_currency_data(initial=False)
        exchange_rates = ExchangeRate.objects.all()
        table = ExchangeRateTable(exchange_rates)
        csv_file_path = "all_currency_data.csv"
        exporter = TableExport("csv", table)
        csv_data = exporter.export()
        with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
            csvfile.write(csv_data)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully exported data to {csv_file_path}")
        )
