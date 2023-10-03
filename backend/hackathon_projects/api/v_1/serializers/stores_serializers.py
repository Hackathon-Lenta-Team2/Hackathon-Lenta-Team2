from rest_framework.serializers import ModelSerializer

from stores.models import City, Division, Format, Location, Size, Store


class CitySerializer(ModelSerializer):
    """Сериализатор для модели City."""

    class Meta:
        model = City
        fields = "__all__"


class DivisionSerializer(ModelSerializer):
    """Сериализатор для модели Division."""

    class Meta:
        model = Division
        fields = "__all__"


class FormatSerializer(ModelSerializer):
    """Сериализатор для модели Format."""

    class Meta:
        model = Format
        fields = "__all__"


class LocationSerializer(ModelSerializer):
    """Сериализатор для модели Location."""

    class Meta:
        model = Location
        fields = "__all__"


class SizeSerializer(ModelSerializer):
    """Сериализатор для модели Size."""

    class Meta:
        model = Size
        fields = "__all__"


class StoreSerializer(ModelSerializer):
    """Сериализатор для модели Store."""

    class Meta:
        model = Store
        fields = "__all__"
