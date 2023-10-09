import io
from typing import Any

import pandas as pd
from django.db.models import QuerySet
from django.http import HttpResponse
from forecasts.models import Forecast, ForecastData
from sales.models import Sale


class ExelExport:
    """
    Класс экспорта данных в виде Excel таблицы.
    Файл прикрепляется к HttpResponse.
    На вход принимает:
    - queryset: QuerySet[Forecast | Sale]
    - Флаг is_forecast: bool - содержит ли queryset данные прогнозов.
    """

    def __init__(self, queryset: QuerySet, is_forecast: bool = True) -> None:
        self.queryset: QuerySet[Forecast | Sale] = queryset
        self.is_forecast: bool = is_forecast
        self.output = io.BytesIO()
        self.data = None

    def export(self) -> HttpResponse:
        if self.is_forecast:
            return self._get_forecast_response()
        return self._get_fact_sales_response()

    def _get_fact_sales_response(self) -> HttpResponse:
        self.data = self._get_sales_data()
        return self._make_excel_file_response(self.data)

    def _get_sales_data(self) -> list[dict]:
        """Собирает список словарей с данными продаж."""
        self.data = []
        for sale in self.queryset:
            sale_info = sale.sale_info.all()
            for info in sale_info:
                row = {
                    "store_id": sale.store_id_id,
                    "pr_sku_id": sale.sku_id_id,
                    "date": info.date,
                    "sales_type": int(info.sales_type),
                    "sales_units": info.sales_units,
                    "sales_units_promo": info.sales_units_promo,
                    "sales_rub": info.sales_rub,
                    "sales_rub_promo": info.sales_rub_promo,
                }
                self.data.append(row)
        return self.data

    def _get_forecast_response(self) -> HttpResponse:
        data = {"Store ID": [], "SKU ID": [], "Forecast Date": []}
        sales_units_data = {}
        self._make_forecast_columns_for_the_table(sales_units_data, data)
        self._make_forecast_rows_for_the_table(sales_units_data, data)
        response = self._make_excel_file_response(data)
        return response

    def _make_forecast_columns_for_the_table(
        self, sales_units_data: dict, data: dict[str, list]
    ) -> dict[str, list]:
        """Создаёт столбцы в таблице excel."""

        for forecast in self.queryset:
            forecast_data = ForecastData.objects.get(forecast_id=forecast)
            sales_units = forecast_data.data

            for date, value in sales_units.items():
                if date not in sales_units_data:
                    sales_units_data[date] = []
                sales_units_data[date].append(value)

        for date in sales_units_data.keys():
            data[date] = []

        return data

    def _make_forecast_rows_for_the_table(self, sales_units_data, data):
        """Создаёт строки в таблице excel."""

        for forecast in self.queryset:
            data["Store ID"].append(forecast.store)
            data["SKU ID"].append(forecast.sku)
            data["Forecast Date"].append(
                forecast.forecast_date.strftime("%Y-%m-%d")
            )

            forecast_data = ForecastData.objects.get(forecast_id=forecast)
            sales_units = forecast_data.data
            for date in sales_units_data.keys():
                data[date].append(sales_units.get(date, None))

    def _make_excel_file_response(self, data: Any) -> HttpResponse:
        """Создаёт HttpResponse с файлом excel."""

        df = pd.DataFrame(data)
        with pd.ExcelWriter(self.output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)
        response = HttpResponse(
            self.output.getvalue(), content_type="application/ms-excel"
        )
        response["Content-Disposition"] = 'attachment; filename="output.xlsx"'

        return response


def export_to_exc_for_dates_filters(filtered_data):
    """Функция записи отфильтрованных по дате данных в excel."""

    data = {
        'Store ID': [],
        'SKU ID': [],
        'Forecast Date': []
    }

    for item in filtered_data:
        data['Store ID'].append(item['store'])
        data['SKU ID'].append(item['sku'])
        data['Forecast Date'].append(item['forecast_date'])

        for date, value in item['forecast_data'][0]['data'].items():
            if date not in data:
                data[date] = []
            data[date].append(value)

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    response = HttpResponse(
        output.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="output.xlsx"'

    return response
