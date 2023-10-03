from django.urls import include, path
from rest_framework import routers

from api.v_1.views.forecasts_views import ForecastViewSet, ImportDataView
from api.v_1.views.profile_views import profile_view
from api.v_1.views.sales_views import SalesViewSet
from api.v_1.views.sku_views import (CategoryViewSet, GroupViewSet,
                                     StockKeepingUnitViewSet,
                                     SubcategoryViewSet)
from api.v_1.views.stores_views import (CityViewSet, DivisionViewSet,
                                        FormatViewSet, StoreViewSet)

app_name = "api"

router = routers.DefaultRouter()
router.register("cities", CityViewSet, basename="cities")
router.register("divisions", DivisionViewSet, basename="divisions")
router.register("formats", FormatViewSet, basename="formats")
router.register("stores", StoreViewSet, basename="stores")
router.register("products", StockKeepingUnitViewSet, basename="products")
router.register("forecasts", ForecastViewSet, basename="forecasts")
router.register("sales", SalesViewSet, basename="sales"),
router.register('groups', GroupViewSet, basename='groups'),
router.register('categories', CategoryViewSet, basename='categories'),
router.register('subcategories', SubcategoryViewSet, basename='subcategories')

urlpatterns = [
    path("", include(router.urls)),
    path("import-data/", ImportDataView.as_view(), name="import-data"),
    path("profile/", profile_view, name="profile")
]
