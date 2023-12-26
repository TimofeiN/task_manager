from typing import Any

from factory import Factory, Faker

from main.models import User


class UserFactory(Factory):
    class Meta:
        model = dict

    username = Faker("user_name")
    role = Faker("random_element", elements=User.Roles.values)
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
