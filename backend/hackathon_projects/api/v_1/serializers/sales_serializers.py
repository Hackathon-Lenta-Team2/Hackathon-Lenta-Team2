from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from sales.models import Sale, SaleInfo


class SaleInfoSerializer(ModelSerializer):
    """Сериализатор для модели SaleInfo."""

    sales_type = SerializerMethodField()

    @staticmethod
    def get_sales_type(sale_info: SaleInfo) -> int:
        return int(sale_info.sales_type)

    class Meta:
        model = SaleInfo
        fields = (
            "date",
            "sales_type",
            "sales_units",
            "sales_units_promo",
            "sales_rub",
            "sales_rub_promo",
        )


class SaleSerializer(ModelSerializer):
    """Сериализатор для модели Sale."""

    fact = SaleInfoSerializer(many=True, source="sale_info")

    class Meta:
        model = Sale
        fields = ("store_id", "sku_id", "fact")
