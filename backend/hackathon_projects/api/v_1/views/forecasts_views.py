from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v_1.filters import ForecastFilter
from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.forecasts_serializers import ForecastSerializer
from core.utils.excel_writer import export_to_excel
from core.utils.json_data_import import import_data_from_json
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

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        export_to_excel(queryset)


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
