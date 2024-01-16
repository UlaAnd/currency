from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import ColumnVisibilityForm
from .models import ExchangeRate
from .tables import ExchangeRateTable


def exchange_rate(request: HttpRequest) -> HttpResponse:
    queryset = ExchangeRate.objects.all()
    table = ExchangeRateTable(queryset)
    return render(request, "currency.html", {"table": table})


def exchange_rate_table(request: HttpRequest) -> HttpResponse:
    invisible_columns = [
        "eur_to_pln",
        "usd_to_pln",
        "chf_to_pln",
        "eur_to_usd",
        "chf_to_usd",
    ]
    if request.method == "POST":
        form = ColumnVisibilityForm(request.POST)
        if form.is_valid():
            invisible_columns = [
                field_name
                for field_name, is_visible in form.cleaned_data.items()
                if not is_visible
            ]
            table = ExchangeRateTable(
                ExchangeRate.objects.all(), exclude=invisible_columns
            )
            form = ColumnVisibilityForm(
                initial={field: False for field in invisible_columns}
            )
            return render(
                request, "exchange_rate_table.html", {"table": table, "form": form}
            )
    table = ExchangeRateTable(ExchangeRate.objects.all(), exclude=invisible_columns)
    form = ColumnVisibilityForm(initial={field: False for field in invisible_columns})
    return render(request, "exchange_rate_table.html", {"table": table, "form": form})
