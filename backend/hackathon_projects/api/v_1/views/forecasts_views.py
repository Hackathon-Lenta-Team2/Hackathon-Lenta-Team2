from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.forecasts_serializers import (
    ForecastSerializer,
    JSONFileSerializer,
)
from core.utils.json_data_import import import_data_from_json
from forecasts.models import Forecast


class ForecastViewSet(ListObjectsMixin):
    """Класс представления для Прогнозов."""

    serializer_class = ForecastSerializer
    queryset = Forecast.objects.all()


class ImportDataView(APIView):
    """Вьюсет импорта данных прогнозов в БД."""

    def post(self, request):
        try:
            if "file" in request.FILES:
                json_file = request.FILES["file"]
                import_data_from_json(json_file)
            else:
                serializer = JSONFileSerializer(data=request.data)
                if serializer.is_valid():
                    file_path = serializer.validated_data.get(
                        "file_path", "forecast_archive.json"
                    )
                    import_data_from_json(file_path)
                else:
                    return Response(
                        {"message": "Не найден файл"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"message": "Данные успешно импортированы"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as err:
            error_message = f"Unexpected {err=}"
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )
