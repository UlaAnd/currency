import statistics
from datetime import date, datetime, timedelta
from typing import List

import requests
from django.db.models import Avg, Max, Q
from requests import HTTPError

from currency_app.models import ExchangeRate


class CurrencyController:
    def fetching_currency_data(self, initial: bool = True) -> None:
        currencies = ["EUR", "USD", "CHF"]
        end_date = datetime.now().date()
        if initial:
            start_date = end_date - timedelta(days=90)
        else:
            start_date = self.get_start_date(end_date)
        for currency in currencies:
            try:
                rates_data = self.get_currency_rates_for_period(
                    code=currency, start_date=start_date, end_date=end_date
                )
            except HTTPError as e:
                print(f"Couldn't fetch rates: {e} ")
                return
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

    def get_currency_rates_for_period(
        self, code: str, start_date: date, end_date: date
    ) -> List:
        url = f"http://api.nbp.pl/api/exchangerates/rates/A/{code}/{start_date}/{end_date}/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = data["rates"]
        return rates

    def get_start_date(self, end_date: date) -> date:
        newest_date = ExchangeRate.objects.aggregate(Max("date"))["date__max"]
        if newest_date:
            days_number = (end_date - newest_date).days
        if days_number > 1:
            start_date = end_date - timedelta(days=days_number - 1)
        else:
            start_date = end_date
        return start_date

    def currency_converter(self) -> None:
        filled_instances = ExchangeRate.objects.filter(
            Q(usd_to_pln__isnull=False)
            & Q(eur_to_pln__isnull=False)
            & Q(chf_to_pln__isnull=False)
            & Q(eur_to_usd__isnull=True)
            & Q(chf_to_usd__isnull=True)
        )
        for instance in filled_instances:
            try:
                instance.eur_to_usd = round(
                    (instance.eur_to_pln / instance.usd_to_pln), 4
                )
                instance.chf_to_usd = round(
                    (instance.chf_to_pln / instance.usd_to_pln), 4
                )
                instance.save()
            except ZeroDivisionError as zd_error:
                print(f"Error: {zd_error}. Skipping instance {instance.pk}")


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
