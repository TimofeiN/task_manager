from typing import Union, List
from http import HTTPStatus
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user(cls)
        cls.client = APIClient()

    @staticmethod
    def create_api_user(cls):
        return User.objects.create(**cls.user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(
        self, data: dict, args: List[Union[str, int]] = None, format: str = None
    ) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.post(self.list_url(args), data=data, format=format)
        assert response.status_code == HTTPStatus.CREATED
        return response.data

    def retrieve(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.detail_url(args))
        assert response.status_code == HTTPStatus.OK
        return response.data

    def delete(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url(args))
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response

    def list(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url(args))
        assert response.status_code == HTTPStatus.OK
        return response.data

    def update(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.put(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK
        return response.data
