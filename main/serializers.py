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
    tag = TagSerializer(many=True, required=False)
    author = UserSerializer(required=False)
    executor = UserSerializer(required=False)

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

    def create(self, data_to_create: dict) -> Task:
        for key in ["author", "executor"]:
            if key in data_to_create:
                user_data = data_to_create.get(key)
                user = User.objects.create(**user_data)
                data_to_create[key] = user
        if "tag" in data_to_create:
            tag_list = data_to_create.pop("tag")
            tag_instance_list = []
            for tag in tag_list:
                tag_instance = Tag.objects.create(**tag)
                tag_instance_list.append(tag_instance)
            task = Task.objects.create(**data_to_create)
            task.tag.set(tag_instance_list)
        else:
            task = Task.objects.create(**data_to_create)
        return task
