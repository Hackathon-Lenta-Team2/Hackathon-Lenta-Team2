from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


class ListObjectsMixin(GenericViewSet, ListModelMixin):
    """Миксин для получения списка объектов модели."""
