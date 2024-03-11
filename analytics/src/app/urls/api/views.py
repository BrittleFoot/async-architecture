from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pass
