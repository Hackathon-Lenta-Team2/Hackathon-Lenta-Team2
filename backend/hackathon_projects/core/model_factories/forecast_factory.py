from datetime import datetime

import factory

from core.model_factories.sku_factory import StockKeepingUnitFactory
from core.model_factories.store_factory import StoreFactory
from forecasts.models import Forecast


class ForecastFactory(factory.django.DjangoModelFactory):
    store = factory.SubFactory(StoreFactory)
    sku = factory.SubFactory(StockKeepingUnitFactory)
    forecast_date = factory.LazyFunction(datetime.now)

    class Meta:
        model = Forecast
