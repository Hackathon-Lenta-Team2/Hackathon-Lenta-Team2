from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.sales_serializers import SaleSerializer
from core.utils.json_fact_sales_import import import_fact_sales_from_json
from sales.models import Sale, SaleInfo


class SalesViewSet(ListObjectsMixin):
    """Класс представления для Продаж."""

    serializer_class = SaleSerializer

    def get_query_params(self) -> tuple[str | None, ...]:
        store_id = self.request.query_params.get("store")
        sku_id = self.request.query_params.get("sku")
        date_after = self.request.query_params.get("date_after")
        date_before = self.request.query_params.get("date_before")
        return store_id, sku_id, date_after, date_before

    def get_queryset(self):
        store_id, sku_id, date_after, date_before = self.get_query_params()
        if not all((store_id, sku_id)):
            raise ValidationError(
                detail={
                    "detail": (
                        "Неверные параметры запроса: 'store' и 'sku' должны "
                        "иметь значения."
                    ),
                }
            )
        sales = Sale.objects.filter(store_id=store_id, sku_id=sku_id)

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


@api_view(("post",))
@permission_classes((IsAuthenticated,))
def sales_import_view(request: Request):
    """Импорт данных фактических продаж."""
    json_file = request.POST["data"]
    print(type(json_file))
    import_fact_sales_from_json(json_file)
    print("HELLLO" * 10)
    return Response(status=status.HTTP_200_OK)
