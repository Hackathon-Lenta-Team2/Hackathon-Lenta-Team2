from datetime import datetime

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.forecasts_serializers import ForecastSerializer
from core.utils.date_filters import filter_forecast_data
from core.utils.excel_writer import (export_to_exc_for_dates_filters,
                                     export_to_excel)
from core.utils.json_data_import import import_data_from_json
from forecasts.models import Forecast


class ForecastViewSet(ListObjectsMixin):
    """Класс представления для Прогнозов."""

    serializer_class = ForecastSerializer

    def list(self, request):
        queryset = Forecast.objects.all()

        sku_id = self.request.query_params.getlist("sku")
        store_id = self.request.query_params.getlist("store")
        date_param = self.request.query_params.getlist("date")
        start_date_param = request.GET.get('start_date', None)
        end_date_param = request.GET.get('end_date', None)

        queryset = Forecast.objects.all()

        if store_id:
            queryset = queryset.filter(store__in=store_id)

        if sku_id:
            queryset = queryset.filter(sku__in=sku_id)

        if date_param:
            dates = [datetime.fromisoformat(date) for date in date_param]
            queryset = queryset.filter(forecast_date__in=dates)

        filtered_queryset = queryset
        if request.GET.get('export') == 'true':
            if start_date_param and end_date_param:
                filtered_data = filter_forecast_data(
                    request, queryset=filtered_queryset)
                return export_to_exc_for_dates_filters(filtered_data)
            return export_to_excel(filtered_queryset)
        if start_date_param and end_date_param:
            filtered_data = filter_forecast_data(
                request, queryset=filtered_queryset)
            return JsonResponse(filtered_data, safe=False)
        else:
            serialized_data = ForecastSerializer(filtered_queryset, many=True)
            return Response(serialized_data.data)


class ImportDataView(APIView):
    """Вьюсет импорта данных прогнозов в БД."""

    def get(self, request):
        try:
            import_data_from_json("forecast_archive.json")
            return Response(
                {'message': 'Данные успешно импортированы'},
                status=status.HTTP_200_OK
            )
        except Exception as err:
            error_message = f"Unexpected {err=}"
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
