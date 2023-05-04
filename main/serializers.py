from rest_framework import serializers
from .models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "role")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title", "unique_id")


class TaskSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    author = UserSerializer()
    executor = UserSerializer()

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "date_created",
            "date_updated",
            "date_to_finish",
            "condition",
            "priority",
            "author",
            "executor",
            "tag",
        )
