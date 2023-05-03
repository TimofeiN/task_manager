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

    def test_create(self) -> dict:
        user = self.create(self.test_user_attributes)
        expected_response = self.expected_details(user, self.test_user_attributes)
        assert user == expected_response
        return user

    def test_retrive(self) -> None:
        user = self.test_create()
        new_user_id = user["id"]
        response = self.retrive(new_user_id)
        assert response == user

    def test_delete(self) -> None:
        user = self.test_create()
        new_user_id = user["id"]
        response = self.delete(new_user_id)
        assert response.content == b""

    def test_list(self) -> None:
        self.test_create()
        response = self.list()
        assert len(response) == 2

    def test_update(self) -> None:
        user = self.test_create()
        new_user_id = user["id"]
        user_name = user["username"]
        updated_name = "Max"
        response = self.update(
            {"username": user_name, "first_name": updated_name}, new_user_id
        )
        assert response["first_name"] == updated_name
