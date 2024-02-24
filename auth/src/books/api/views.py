from books.api.serializers import BookSerializer
from books.models import Book
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class BookViewSet(ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope,
    ]
    serializer_class = BookSerializer
    queryset = Book.objects.all()
