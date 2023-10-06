import pandas as pd
import xlsxwriter
from django.http import HttpResponse
from forecasts.models import ForecastData


def export_to_excel(queryset):
    """Функция записи данных в excel."""

    data = {
        'Store ID': [],
        'SKU ID': [],
        'Forecast Date': []
    }

    sales_units_data = {}

    _make_columns_for_the_table(sales_units_data, queryset, data)
    _make_rows_for_the_table(sales_units_data, queryset, data)
    response = _make_excel_file(data)

    return response


def _make_columns_for_the_table(sales_units_data, queryset, data):
    """Функция создания столбцов в таблице excel."""

    for forecast in queryset:
        forecast_data = ForecastData.objects.get(forecast_id=forecast)
        sales_units = forecast_data.data

        for date, value in sales_units.items():
            if date not in sales_units_data:
                sales_units_data[date] = []
            sales_units_data[date].append(value)

    for date in sales_units_data.keys():
        data[date] = []

    return data


def _make_rows_for_the_table(sales_units_data, queryset, data):
    """Функция создания строк в таблице excel."""

    for forecast in queryset:
        data['Store ID'].append(forecast.store)
        data['SKU ID'].append(forecast.sku)
        data['Forecast Date'].append(
            forecast.forecast_date.strftime('%Y-%m-%d'))

        forecast_data = ForecastData.objects.get(forecast_id=forecast)
        sales_units = forecast_data.data
        for date in sales_units_data.keys():
            data[date].append(sales_units.get(date, None))

    return data


def _make_excel_file(data):
    """Функция создания файла excel."""

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    response = HttpResponse(
        output.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="output.xlsx"'

    return response
