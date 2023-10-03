from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.forecasts_serializers import ForecastSerializer
from core.utils.json_data_import import import_data_from_json
from forecasts.models import Forecast


class ForecastViewSet(ListObjectsMixin):
    """Класс представления для Прогнозов."""

    serializer_class = ForecastSerializer
    queryset = Forecast.objects.all()


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
