from base import TestViewSetBase


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "is_staff": True,
    }
    test_tag_attributes = {
        "title": "tag_for_test",
        "unique_id": 1111,
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def test_create(self) -> None:
        tag = self.create(self.test_tag_attributes)
        expected_response = self.expected_details(tag, self.test_tag_attributes)
        assert tag == expected_response
        return tag

    def test_retrive(self) -> None:
        tag = self.test_create()
        new_tag_id = tag["id"]
        response = self.retrive(new_tag_id)
        assert response == tag

    def test_delete(self) -> None:
        tag = self.test_create()
        new_tag_id = tag["id"]
        response = self.delete(new_tag_id)
        assert response.content == b""

    def test_list(self) -> None:
        self.test_create()
        response = self.list()
        assert len(response) == 1

    def test_update(self) -> None:
        tag = self.test_create()
        new_tag_id = tag["id"]
        title_to_update = "updated_tag"
        response = self.update({"title": title_to_update}, new_tag_id)
        assert response["title"] == title_to_update
