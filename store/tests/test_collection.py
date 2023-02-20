from store.models import Collection
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestPostCollection:
    def test_if_user_is_anonymouse_returns_401(self):
        # arange
        # act
        client = APIClient()
        response = client.post('/store/collections/', {'title': 'a'})
        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_returns_403(self):
        # act
        client = APIClient()
        # arange
        client.force_authenticate(user={}) 
        response = client.post('/store/collections/', {'title': 'a'})
        # assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_not_valid_returns_400(self):
        # arange
        # act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': ''})
        # assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self):
        # arange
        # act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': 'a'})
        new_built_collection_id = response.data['id']
        get_response = client.get(f'/store/collections/{new_built_collection_id}/')
        # assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == get_response.data['id']

@pytest.mark.django_db
class TestRetireveCollection:
    def test_if_collection_exists_returns_200(self):
        client = APIClient()
        collection = baker.make(Collection)

        response = client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }

    def test_if_collection_does_not_exists_returns_404(self):
        client = APIClient()

        wrong_id = 1000

        response = client.get(f'/store/collections/{wrong_id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] is not None

        