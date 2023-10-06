from django.db.models import Prefetch
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.sales_serializers import (
    FactSalesFileSerializer,
    SaleSerializer,
)
from core.utils.excel_writer import ExelExport
from sales.models import FactSalesFile, Sale, SaleInfo


class SalesViewSet(ListObjectsMixin):
    """Класс представления для Продаж."""

    serializer_class = SaleSerializer

    def get_query_params(self) -> tuple[list | None, list | None, str, str]:
        stores = self.request.query_params.getlist("store")
        products = self.request.query_params.getlist("sku")
        date_after = self.request.query_params.get("date_after")
        date_before = self.request.query_params.get("date_before")
        return stores, products, date_after, date_before

    def get_queryset(self):
        stores, products, date_after, date_before = self.get_query_params()
        if not all((stores, products)):
            raise ValidationError(
                detail={
                    "detail": (
                        "Неверные параметры запроса: 'store' и 'sku' должны "
                        "иметь значения."
                    ),
                }
            )

        sales = Sale.objects.filter(store_id__in=stores, sku_id__in=products)

        if all((date_after, date_before)):
            return sales.prefetch_related(
                Prefetch(
                    "sale_info",
                    queryset=SaleInfo.objects.filter(
                        date__gte=date_after, date__lte=date_before
                    ),
                )
            )
        if date_after:
            return sales.prefetch_related(
                Prefetch(
                    "sale_info",
                    queryset=SaleInfo.objects.filter(date__gte=date_after),
                )
            )
        if date_before:
            return sales.prefetch_related(
                Prefetch(
                    "sale_info",
                    queryset=SaleInfo.objects.filter(date__lte=date_before),
                )
            )
        return sales.prefetch_related("sale_info")

    @action(url_path="export", detail=False, methods=["get"])
    def export_excel(self, request):
        queryset = self.get_queryset()
        response = ExelExport(queryset, is_forecast=False).export()
        return response


class FactSalesImportViewSet(ModelViewSet):
    """Класс представления для загрузки файла фактических продаж."""

    queryset = FactSalesFile.objects.all()
    serializer_class = FactSalesFileSerializer
    http_method_names = ("post",)
