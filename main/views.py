from rest_framework import viewsets
from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.prefetch_related("tag")
        .select_related("author")
        .select_related("executor")
        .order_by("id")
    )
    serializer_class = TaskSerializer
