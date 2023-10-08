from django.contrib import admin

from .models import UOM, Category, Group, StockKeepingUnit, Subcategory


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Group."""

    list_display = ("id",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Category."""

    list_display = (
        "id",
        "group_id",
    )
    list_filter = ("group_id",)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Subcategory."""

    list_display = (
        "id",
        "category_id",
    )
    list_filter = ("category_id",)


@admin.register(UOM)
class UOMAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели UOM."""

    list_display = (
        "id",
        "title",
    )
    search_fields = ("title",)


@admin.register(StockKeepingUnit)
class StockKeepingUnitAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели StockKeepingUnit."""

    list_display = ("id", "title", "group_id", "cat_id", "subcat_id", "uom_id")
    list_filter = ("title", "group_id", "cat_id", "subcat_id", "uom_id")
    search_fields = ("title", "group_id", "cat_id", "subcat_id", "uom_id")
