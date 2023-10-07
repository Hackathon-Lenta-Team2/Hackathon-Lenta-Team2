from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v_1.filters import ForecastFilter
from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.forecasts_serializers import ForecastSerializer
from core.services.tasks import ds_data_import_task
from core.utils.excel_writer import ExelExport
from forecasts.models import Forecast


class ForecastViewSet(ListObjectsMixin):
    """Класс представления для Прогнозов."""

    serializer_class = ForecastSerializer
    filter_class = ForecastFilter

    def get_queryset(self):
        sku_id = self.request.query_params.getlist("sku")
        store_id = self.request.query_params.getlist("store")
        date_param = self.request.query_params.getlist("date")
        queryset = Forecast.objects.all()

        if store_id or sku_id or date_param:
            if date_param:
                dates = [datetime.fromisoformat(date) for date in date_param]
                queryset = queryset.filter(forecast_date__in=dates)

            if store_id:
                queryset = queryset.filter(store__in=store_id)

            if sku_id:
                queryset = queryset.filter(sku__in=sku_id)
        # response = export_to_excel(queryset)
        return queryset

    @action(url_path="export", detail=False, methods=["get"])
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        response = ExelExport(queryset, is_forecast=True).export()
        return response


class ImportDataView(APIView):
    """Вьюсет импорта данных прогнозов в БД."""

    def get(self, request):
        try:
            ds_data_import_task.delay()
            return Response(
                {"message": "Операция импорта данных началась."},
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            error_message = f"Unexpected {err=}"
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )
