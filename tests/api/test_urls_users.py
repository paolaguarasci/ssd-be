import json
import os
from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.forms.models import model_to_dict
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Dress, DressLoan


@pytest.fixture
@pytest.mark.django_db
def api_client(django_db_setup):
    user = User.objects.get(username=os.environ['USER_USERNAME'])
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    print("refresh.access_token", refresh.access_token)
    return client


def getClient(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]

def getToday():
    return str(date.today())


def getTodayPlus(days):
    return str(date.today()+timedelta(days=days))


@pytest.mark.django_db
def test_dress_user_get_list(api_client):
    dress = Dress.objects.filter(deleted=False)
    path = reverse('dress-list')
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(dress)


@pytest.mark.django_db
def test_dress_user_get_list_only_noDeleted(api_client):
    path = reverse('dress-list')
    dress = Dress.objects.all()
    Dress.objects.filter(id=dress[0].id).delete()
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == (len(dress)-1)


@pytest.mark.django_db
def test_dress_retrive_a_single_dress(api_client):
    dress = Dress.objects.all()
    path = reverse('dress-detail', kwargs={'id': dress[0].id})
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert obj['id'] == str(dress[0].id)


@pytest.mark.django_db
def test_user_receives_a_list_with_only_his_loan(api_client):
    user = User.objects.get(username=os.environ['USER_USERNAME'])
    dress = Dress.objects.all()
    path = reverse('dressloan-list')
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == 1
    assert obj[0]['loaner'] == user.id

@pytest.mark.django_db
def tests_dress_loan_user_can_post(api_client):
    path = reverse('dressloan-list')
    response = api_client.post(path, {
        "startDate": getToday(),
        "endDate": getTodayPlus(5),
        "dress": "fba6e9a1-1161-4b97-9a34-e474254bb0d8",
        "loaner": 2,
        "totalPrice": 700.0,
        "loanDurationDays": 7,
        "terminated": "false"
    }, secure=True)
    assert response.status_code == HTTP_201_CREATED
    assert contains(response, 'startDate', getToday())


@pytest.mark.django_db
def test_user_cant_update_his_loan(api_client):
    user = User.objects.get(username=os.environ['USER_USERNAME'])
    dressLoan = DressLoan.objects.get(loaner=user.id)
    print(dressLoan)
    path = reverse('dressloan-detail', kwargs={'id': dressLoan.id})
    res = api_client.get(path, secure=True)
    obj = parse(res)
    obj['endDate'] = "2022-12-10"
    path = reverse('dressloan-detail', kwargs={'id': dressLoan.id})
    response = api_client.put(path, obj, secure=True)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_cant_delete_his_loan(api_client):
    user = User.objects.get(username=os.environ['USER_USERNAME'])
    dressLoan = DressLoan.objects.get(loaner=user.id)
    path = reverse('dressloan-detail', kwargs={'id': dressLoan.id})
    response = api_client.delete(path, secure=True)
    assert response.status_code == HTTP_403_FORBIDDEN
