import statistics
from datetime import datetime, timedelta
from typing import List

import requests
from django.db.models import Avg, Q

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
            instance.eur_to_usd = round((instance.eur_to_pln / instance.usd_to_pln), 4)
            instance.chf_to_usd = round((instance.chf_to_pln / instance.usd_to_pln), 4)
            instance.save()


class DataAnalysis:
    PAIR_MODEL_MAPPING = {
        "eur_to_pln": "EUR/PLN",
        "usd_to_pln": "USD/PLN",
        "chf_to_pln": "CHF/PLN",
        "eur_to_usd": "EUR/USD",
        "chf_to_usd": "CHF/USD",
    }

    def calculations(self, selected_pairs: str) -> dict:
        result = {}
        for pair in selected_pairs:
            exchange_rates = ExchangeRate.objects.values_list(pair, flat=True).exclude(
                **{pair: None}
            )
            avg = ExchangeRate.objects.aggregate(Avg(f"{pair}", default=0))
            model_name = self.PAIR_MODEL_MAPPING.get(pair, pair)
            pair_result = {
                "average_rate_value": round(avg.get(f"{pair}__avg"), 4),
                "median_rate": statistics.median(exchange_rates),
                "min_rate": min(exchange_rates),
                "max_rate": max(exchange_rates),
            }
            result[model_name] = pair_result
        return result


if __name__ == "__main__":
    task = CurrencyController()
    task.fetching_currency_data()
