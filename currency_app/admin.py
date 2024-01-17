from django.contrib import admin

from currency_app.models import ExchangeRate


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "eur_to_pln",
        "usd_to_pln",
        "chf_to_pln",
        "eur_to_usd",
        "chf_to_usd",
        "created_at",
        "updated_at",
    )


admin.site.register(ExchangeRate, ExchangeRateAdmin)
