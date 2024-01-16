import django_tables2 as tables

from .models import ExchangeRate


class ExchangeRateTable(tables.Table):
    class Meta:
        model = ExchangeRate
        attrs = {"class": "table table-striped"}

    date = tables.Column(verbose_name="Date", order_by=("date",))
    eur_to_pln = tables.Column(verbose_name="EUR/PLN", order_by=("eur_to_pln",))
    usd_to_pln = tables.Column(verbose_name="USD/PLN", order_by=("usd_to_pln",))
    chf_to_pln = tables.Column(verbose_name="CHF/PLN", order_by=("chf_to_pln",))
    eur_to_usd = tables.Column(verbose_name="EUR/USD", order_by=("eur_to_usd",))
    chf_to_usd = tables.Column(verbose_name="CHF/USD", order_by=("chf_to_usd",))
