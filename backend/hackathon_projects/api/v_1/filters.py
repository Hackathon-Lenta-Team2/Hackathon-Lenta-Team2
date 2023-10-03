from django_filters import rest_framework as filters

from products.models import Category, Group, StockKeepingUnit, Subcategory


class GroupFilter(filters.FilterSet):
    """Фильтр представления для Групп."""

    class Meta:
        model = Group
        fields = ['id']


class CategoryFilter(filters.FilterSet):
    """Фильтр представления для Категорий."""

    class Meta:
        model = Category
        fields = ['group_id']


class SubcategoryFilter(filters.FilterSet):
    """Фильтр представления для Подкатегорий."""

    class Meta:
        model = Subcategory
        fields = ['category_id']


class StockKeepingUnitFilter(filters.FilterSet):
    """Фильтр представления для Товаров."""

    class Meta:
        model = StockKeepingUnit
        fields = ['subcat_id']
