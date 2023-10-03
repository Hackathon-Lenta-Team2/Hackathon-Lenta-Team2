from django.contrib import admin

from .models import City, Division, Format, Location, Size, Store


class CityAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели City."""

    list_display = ("pk", "title")
    list_display_links = list_display
    search_fields = ("title",)


class DivisionAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Division."""

    list_display = ("pk", "title")
    list_display_links = list_display
    search_fields = ("title",)


class FormatAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Format."""

    list_display = ("pk", "title")
    list_display_links = list_display
    search_fields = ("title",)


class LocationAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Location."""

    list_display = ("pk", "type")
    list_display_links = list_display
    search_fields = ("type",)


class SizeAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Size."""

    list_display = ("pk", "type")
    list_display_links = list_display
    search_fields = ("type",)


class StoreAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Store."""

    list_display = (
        "pk",
        "title",
        "city",
        "division",
        "type_format",
        "loc",
        "size",
        "is_active",
    )
    list_display_links = list_display
    search_fields = ("title", "loc", "size", "type_format")


admin.site.register(City, CityAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Format, FormatAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Store, StoreAdmin)
