import json
import os

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.forms.models import model_to_dict
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND)
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Dress, DressLoan


@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'api/fixtures/all.json')


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


@pytest.fixture
@pytest.mark.django_db
def api_client(django_db_setup):
    user = User.objects.get(username=os.environ['SUPERUSER_USERNAME'])
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    print("refresh.access_token", refresh.access_token)
    return client

######################### Users               #############################################

@pytest.mark.django_db
def test_admin_get_all_users_list(api_client):
    path = reverse('user-list')
    user = User.objects.all()
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(user)

@pytest.mark.django_db
def test_user_admin_get_yours(api_client):
    user = User.objects.get(username=os.environ['SUPERUSER_USERNAME'])
    path = reverse('user-detail', kwargs={'id': user.id})
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    assert contains(response, 'username', user.username)

@pytest.mark.django_db
def test_user_admin_get_all_details(api_client):
    user = User.objects.get(username=os.environ['USER_USERNAME'])
    path = reverse('user-detail', kwargs={'id': user.id})
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    assert contains(response, 'username', user.username)

######################### Corner Case - Dress #############################################

@pytest.mark.django_db
def tests_dress_admin_cant_post_alredy_loan_overlap_date(api_client):
    path = reverse('dressloan-list')

    response = api_client.post(path, {
        "startDate": "2022-12-05",
        "endDate": "2022-12-10",
        "dress": "fba6e9a1-1161-4b97-9a34-e474254bb0d8",
        "loaner": 2,
        "totalPrice": 700.0,
        "loanDurationDays": 7,
        "terminated": "false"
    }, secure=True)
    assert response.status_code == HTTP_201_CREATED
    assert contains(response, 'startDate', '2022-12-05')

    response = api_client.post(path, {
        "startDate": "2022-12-05",
        "endDate": "2022-12-10",
        "dress": "fba6e9a1-1161-4b97-9a34-e474254bb0d8",
        "loaner": 2,
        "totalPrice": 700.0,
        "loanDurationDays": 7,
        "terminated": "false"
    }, secure=True)
    
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert contains(response, 'detail', 'Dress already loan')