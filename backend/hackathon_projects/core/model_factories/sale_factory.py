import factory

from core.model_factories.sku_factory import StockKeepingUnitFactory
from core.model_factories.store_factory import StoreFactory
from sales.models import Sale


class SaleFactory(factory.django.DjangoModelFactory):
    store_id = factory.SubFactory(StoreFactory)
    sku_id = factory.SubFactory(StockKeepingUnitFactory)

    class Meta:
        model = Sale
