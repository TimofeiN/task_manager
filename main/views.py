import django_filters

from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.serializers import BaseSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin


class AdminOrReadonly(BasePermission):
    def has_permission(self, request: HttpRequest, view: viewsets.ModelViewSet) -> bool:
        if request.user.is_staff:
            return True
        else:
            return request.method in SAFE_METHODS


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskFilter(django_filters.FilterSet):
    condition = django_filters.ChoiceFilter(
        field_name="condition", choices=Task.Conditions.choices
    )
    tag = django_filters.ModelMultipleChoiceFilter(
        field_name="tag__title",
        to_field_name="title",
        conjoined=True,
        queryset=Tag.objects.all(),
    )
    executor = django_filters.ModelChoiceFilter(
        field_name="executor", queryset=User.objects.all()
    )
    author = django_filters.ModelChoiceFilter(
        field_name="author", queryset=User.objects.all()
    )

    class Meta:
        model = Task
        fields = ["condition", "tag", "executor", "author"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = (IsAuthenticated, AdminOrReadonly)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, AdminOrReadonly)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.prefetch_related("tag")
        .select_related("author")
        .select_related("executor")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = (IsAuthenticated, AdminOrReadonly)


def generate_error(request: HttpRequest) -> None:
    a = None
    a.hello()


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")
    permission_classes = (IsAuthenticated, AdminOrReadonly)

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Task.objects.prefetch_related("tag")
        .select_related("author")
        .select_related("executor")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = (IsAuthenticated, AdminOrReadonly)


class TaskTagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, AdminOrReadonly)

    def get_queryset(self) -> QuerySet:
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tag.all()

    def perform_create(self, serializer: BaseSerializer) -> None:
        tag_obj = serializer.save()
        task_id = self.kwargs["parent_lookup_task_id"]
        Task.objects.get(pk=task_id).tag.add(tag_obj)
