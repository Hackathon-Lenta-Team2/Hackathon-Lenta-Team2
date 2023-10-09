from collections import defaultdict
from datetime import datetime, timedelta

from forecasts.models import ForecastData


def filter_forecast_data(request, queryset=None):
    """Функция фильтрации по промежутку дат."""

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)

    response_data_list = _make_response_data(queryset,
                                             start_date,
                                             end_date)

    return response_data_list


def _make_response_data(queryset, start_date, end_date):
    """
    Функция cоздания словаря для хранения данных.
    Фильтруем данные по датам из заданного диапазона.
    """
    response_data_list = []
    forecast_date_list = []
    for forecast_object in queryset:
        data_by_date = defaultdict(
            lambda: {'forecast_data': [{'data': {}}]})
        filtered_forecast_data = ForecastData.objects.filter(
            forecast_id=forecast_object,
        )
        _check_filtered_data(filtered_forecast_data, forecast_date_list,
                             start_date, end_date, data_by_date, forecast_object)
        filtered_data_list = list(data_by_date.values())

        _make_empty_data(start_date, end_date, forecast_date_list,
                         filtered_data_list, response_data_list, data_by_date)

    return response_data_list


def _check_filtered_data(filtered_forecast_data,
                         forecast_date_list, start_date,
                         end_date, data_by_date,
                         forecast_object):
    """
    Проходим по всем записям в поле data. 
    Проверяем, попадает ли дата в заданный диапазон.
    """
    for forecast_data in filtered_forecast_data:

        for date_str, value in forecast_data.data.items():
            forecast_date = datetime.fromisoformat(date_str)
            forecast_date_list.append(forecast_date)

            if start_date <= forecast_date <= end_date:
                data_by_date[date_str]['store'] = forecast_object.store.id
                data_by_date[date_str]['sku'] = forecast_object.sku.id
                data_by_date[date_str]['forecast_date'] = forecast_object.forecast_date
                data_by_date[date_str]['forecast_data'][0]['data'][date_str] = value


def _make_empty_data(start_date, end_date,
                     forecast_date_list,
                     filtered_data_list,
                     response_data_list,
                     data_by_date):
    """Создаем итоговую запись с данными для дат."""

    if start_date in forecast_date_list and end_date in forecast_date_list:
        all_dates = [start_date + timedelta(days=i)
                     for i in range((end_date - start_date).days + 1)]
        all_dates_str = [date.strftime('%Y-%m-%d') for date in all_dates]

        response_data = {
            'store': filtered_data_list[0]['store'],
            'sku': filtered_data_list[0]['sku'],
            'forecast_date': filtered_data_list[0]['forecast_date'],
            'forecast_data': [{'data': {all_dates_str[0]: 0}}]
        }

        for date_str, data_item in data_by_date.items():
            response_data['forecast_data'][0]['data'][date_str] = data_item['forecast_data'][0]['data'][date_str]
        response_data_list.append(response_data)
