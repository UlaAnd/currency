import django_tables2 as tables
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.export.views import ExportMixin

from .forms import ColumnVisibilityForm
from .models import ExchangeRate
from .tables import ExchangeRateTable


def exchange_rate(request: HttpRequest) -> HttpResponse:
    queryset = ExchangeRate.objects.all()
    table = ExchangeRateTable(queryset)
    RequestConfig(request).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(f"table.{export_format}")

    return render(request, "table.html", {"table": table})


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
            request.session["invisible_columns"] = invisible_columns
    table = ExchangeRateTable(ExchangeRate.objects.all(), exclude=invisible_columns)
    form = ColumnVisibilityForm(initial={field: False for field in invisible_columns})
    export_format = request.GET.get("_export", None)
    if export_format:
        selected_invisible = request.session["invisible_columns"]
        response = export_table(export_format, selected_invisible)
        return response
    else:
        return render(
            request,
            "exchange_rate_table.html",
            {"table": table, "form": form, "test": "huh"},
        )


def export_table(export_format: str, selected_invisible: list) -> HttpResponse:
    if export_format == "csv_all":
        table = ExchangeRateTable(ExchangeRate.objects.all())
        exporter = TableExport("csv", table)
        filename = "all_currency_data.csv"
        confirmation_message = "Data for all currencies has been saved!"

    elif export_format == "csv":
        table = ExchangeRateTable(
            ExchangeRate.objects.all(), exclude=selected_invisible
        )
        exporter = TableExport(export_format, table)
        filename = "selected_currency_data.csv"
        confirmation_message = "Data for selected currencies has been saved!"

    else:
        return None  # Invalid export format
    response = exporter.response(f"table.{export_format}")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response["Content-Type"] = f"text/{export_format}"
    response["confirmation_message"] = confirmation_message
    return response


class TableView(ExportMixin, tables.SingleTableView):
    table_class = ExchangeRateTable
    model = ExchangeRate
    template_name = "exchange_rate_table.html"
    export_formats = ["csv"]
