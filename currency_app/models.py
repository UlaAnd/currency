from django.db import models


class ExchangeRate(models.Model):
    date = models.DateField()
    eur_to_pln = models.FloatField(verbose_name="EUR/PLN", null=True, blank=True)
    usd_to_pln = models.FloatField(verbose_name="USD/PLN", null=True, blank=True)
    chf_to_pln = models.FloatField(verbose_name="CHF/PLN", null=True, blank=True)
    eur_to_usd = models.FloatField(verbose_name="EUR/USD", null=True, blank=True)
    chf_to_usd = models.FloatField(verbose_name="CHF/USD", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            f"{self.date} - EUR/PLN: {self.eur_to_pln}, USD/PLN: {self.usd_to_pln}, CHF/PLN: {self.chf_to_pln}, "
            f" EUR/USD: {self.eur_to_usd},  CHF/USD: {self.chf_to_usd}"
        )
