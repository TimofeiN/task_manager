from typing import Any

from main.models import User, Task
from test.fixtures.factories import UserFactory, TaskFactory


class UserResource:
    factory = UserFactory

    def create(self, **kwargs: Any) -> User:
        attributes = self.factory.build(**kwargs)
        return User.objects.create_user(**attributes)


class TaskResource:
    factory = TaskFactory

    def create(self, **kwargs: Any) -> Task:
        attributes = self.factory.build(**kwargs)
        return Task.objects.create(**attributes)
