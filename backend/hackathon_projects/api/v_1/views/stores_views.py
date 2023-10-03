from rest_framework.filters import SearchFilter

from api.v_1.mixins import ListObjectsMixin
from api.v_1.serializers.stores_serializers import (CitySerializer,
                                                    DivisionSerializer,
                                                    FormatSerializer,
                                                    StoreSerializer)
from stores.models import City, Division, Format, Store


class CityViewSet(ListObjectsMixin):
    """Класс представления для Городов."""

    serializer_class = CitySerializer
    queryset = City.objects.all()


class DivisionViewSet(ListObjectsMixin):
    """Класс представления для Подразделений."""

    serializer_class = DivisionSerializer
    queryset = Division.objects.all()


class FormatViewSet(ListObjectsMixin):
    """Класс представления для Форматов типа супермаркета."""

    serializer_class = FormatSerializer
    queryset = Format.objects.all()


class StoreViewSet(ListObjectsMixin):
    """Класс представления для Супермаркетов."""

    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = (
        "title",
        "city__title",
        "division__title",
        "type_format__title",
        "loc__type",
        "size__type",
    )
