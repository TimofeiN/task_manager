from typing import Union, List
from http import HTTPStatus

from django.http import HttpResponse
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import User
from test.utils.action_client import ActionClient


class TestViewSetBase(APITestCase):
    user: User = None
    api_client: APIClient = None
    action_client: ActionClient
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.api_client = APIClient()
        cls.action_client = ActionClient(cls.api_client)
        cls.action_client.init_user()
        cls.user = cls.action_client.user

    def setUp(self) -> None:
        self.api_client.force_authenticate(self.user)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(
        self, data: dict, args: List[Union[str, int]] = None, format: str = None
    ) -> dict:
        print(self.api_client, self.user)
        response = self.api_client.post(self.list_url(args), data=data, format=format)
        assert response.status_code == HTTPStatus.CREATED
        return response.data

    def retrieve(self, args: Union[str, int] = None) -> dict:
        response = self.api_client.get(self.detail_url(args))
        assert response.status_code == HTTPStatus.OK
        return response.data

    def delete(self, args: Union[str, int] = None) -> HttpResponse:
        response = self.api_client.delete(self.detail_url(args))
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response

    def list(self, args: List[Union[str, int]] = None) -> dict:
        response = self.api_client.get(self.list_url(args))
        assert response.status_code == HTTPStatus.OK
        return response.data

    def update(self, data: dict, args: Union[str, int] = None) -> dict:
        response = self.api_client.put(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK
        return response.data
