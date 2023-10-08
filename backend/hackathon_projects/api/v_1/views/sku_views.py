from api.v_1.filters import (
    CategoryFilter,
    GroupFilter,
    StockKeepingUnitFilter,
    SubcategoryFilter,
)
from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.products_serializers import (
    CategorySerializer,
    GroupSerializer,
    StockKeepingUnitSerializer,
    SubcategorySerializer,
)
from products.models import Category, Group, StockKeepingUnit, Subcategory


class GroupViewSet(ListObjectsMixin):
    """Класс представления для Групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_class = GroupFilter


class CategoryViewSet(ListObjectsMixin):
    """Класс представления для Категорий."""

    serializer_class = CategorySerializer
    filter_class = CategoryFilter

    def get_queryset(self):
        group_id = self.request.query_params.getlist("group_id")
        if group_id:
            return Category.objects.filter(group_id__in=group_id)
        else:
            return Category.objects.all()


class SubcategoryViewSet(ListObjectsMixin):
    """Класс представления для Подкатегорий."""

    serializer_class = SubcategorySerializer
    filter_class = SubcategoryFilter

    def get_queryset(self):
        category_id = self.request.query_params.getlist("category_id")
        if category_id:
            return Subcategory.objects.filter(category_id__in=category_id)
        else:
            return Subcategory.objects.all()


class StockKeepingUnitViewSet(ListObjectsMixin):
    """Класс представления для Товаров."""

    serializer_class = StockKeepingUnitSerializer
    filter_class = StockKeepingUnitFilter

    def get_queryset(self):
        subcat_id = self.request.query_params.getlist("subcat_id")
        if subcat_id:
            return StockKeepingUnit.objects.filter(subcat_id__in=subcat_id)
        else:
            return StockKeepingUnit.objects.all()
