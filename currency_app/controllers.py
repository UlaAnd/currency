from datetime import datetime, timedelta
from typing import List

import requests
from django.db.models import Q

from currency_app.models import ExchangeRate


class CurrencyController:
    def get_currency_rates_for_period(self, code: str, days: int = 90) -> List:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        url = f"http://api.nbp.pl/api/exchangerates/rates/A/{code}/{start_date}/{end_date}/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = data["rates"]
        return rates

    def fetching_currency_data(self) -> None:
        currencies = ["EUR", "USD", "CHF"]
        for currency in currencies:
            rates_data = self.get_currency_rates_for_period(code=currency)

            for rate in rates_data:
                date_str = rate.get("effectiveDate")
                if date_str:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    obj, created = ExchangeRate.objects.update_or_create(
                        date=date,
                        defaults={f"{currency.lower()}_to_pln": rate.get("mid")},
                    )
                    if created:
                        print(
                            f"New ExchangeRate object created for {currency} on {date}"
                        )
                    else:
                        print(f"ExchangeRate object updated for {currency} on {date}")
        self.currency_converter()

    def currency_converter(self) -> None:
        filled_instances = ExchangeRate.objects.filter(
            Q(usd_to_pln__isnull=False)
            & Q(eur_to_pln__isnull=False)
            & Q(chf_to_pln__isnull=False)
        )
        for instance in filled_instances:
            instance.eur_to_usd = instance.eur_to_pln / instance.usd_to_pln
            instance.chf_to_usd = instance.chf_to_pln / instance.usd_to_pln
            instance.save()


if __name__ == "__main__":
    task = CurrencyController()
    task.fetching_currency_data()
