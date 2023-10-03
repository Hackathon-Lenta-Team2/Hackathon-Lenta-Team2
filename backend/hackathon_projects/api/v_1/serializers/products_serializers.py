from rest_framework.serializers import ModelSerializer

from products.models import UOM, Category, Group, StockKeepingUnit, Subcategory


class GroupSerializer(ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = "__all__"


class SubcategorySerializer(ModelSerializer):
    """Сериализатор для модели Subcategory."""

    class Meta:
        model = Subcategory
        fields = "__all__"


class UOMSerializer(ModelSerializer):
    """Сериализатор для модели UOM."""

    class Meta:
        model = UOM
        fields = "__all__"


class StockKeepingUnitSerializer(ModelSerializer):
    """Сериализатор для модели StockKeepingUnit."""

    class Meta:
        model = StockKeepingUnit
        fields = "__all__"
