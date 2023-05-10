from rest_framework.utils.serializer_helpers import ReturnDict

from base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "is_staff": True,
    }

    test_user_attributes = {
        "username": "johnsmith_2",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"], "role": entity["role"]}

    def test_create(self) -> ReturnDict:
        user = self.create(self.test_user_attributes)
        expected_response = self.expected_details(user, self.test_user_attributes)
        assert user == expected_response
        return user

    def test_retrieve(self) -> None:
        user = self.test_create()
        new_user_id = user["id"]
        response = self.retrieve(new_user_id)
        assert response == user

    def test_list(self) -> None:
        new_user = self.test_create()
        api_user = self.retrieve(self.user.id)
        response = self.list()
        assert len(response) == 2
        assert api_user in response
        assert new_user in response

    def test_update(self) -> None:
        user = self.test_create()
        new_user_id = user["id"]
        user_name = user["username"]
        updated_name = "Max"
        response = self.update(
            {"username": user_name, "first_name": updated_name}, new_user_id
        )
        assert response["first_name"] == updated_name

    def test_delete(self) -> None:
        new_user = self.test_create()
        users_list = self.list()
        assert new_user in users_list

        new_user_id = new_user["id"]
        response = self.delete(new_user_id)
        new_users_list = self.list()
        assert response.content == b""
        assert new_user not in new_users_list
