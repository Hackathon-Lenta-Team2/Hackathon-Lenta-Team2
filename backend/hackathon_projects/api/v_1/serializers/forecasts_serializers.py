from rest_framework.serializers import ModelSerializer

from forecasts.models import Forecast, ForecastData


class ForecastDataSerializer(ModelSerializer):
    """Сериализатор для модели ForecastDate."""

    class Meta:
        model = ForecastData
        fields = ['data']


class ForecastSerializer(ModelSerializer):
    """Сериализатор для модели Forecast."""

    forecast_data = ForecastDataSerializer(
        many=True, read_only=True, source='forecastdata_set')

    class Meta:
        model = Forecast
        fields = ['store', 'sku', 'forecast_date', 'forecast_data']

    # def get_forecast_data(self, obj):
    #     forecast_data_date = self.context.get('forecast_data_date')
    #     filtered_data = {date: value for date, value in obj.forecast_data.data.items(
    #     ) if date == forecast_data_date}
    #     return [{'data': filtered_data}]
