from django.contrib import admin

from .models import FactSalesFile, Sale, SaleInfo


class SaleAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Sale."""

    list_display = ("pk", "store_id", "sku_id")
    list_display_links = list_display


class SaleInfoAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели SaleInfo."""

    list_display = (
        "pk",
        "sale_id",
        "date",
        "sales_type",
        "sales_units",
        "sales_units_promo",
        "sales_rub",
        "sales_rub_promo",
    )
    list_display_links = ("pk", "sale_id", "date")
    list_filter = ("date",)
    list_editable = (
        "sales_type",
        "sales_units",
        "sales_units_promo",
        "sales_rub",
        "sales_rub_promo",
    )


class FactSalesFileAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели FactSalesFile."""

    list_display = ("pk", "file_path")
    list_display_links = list_display


admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleInfo, SaleInfoAdmin)
admin.site.register(FactSalesFile, FactSalesFileAdmin)
