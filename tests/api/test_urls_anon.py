import json

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient

from api.models import Dress, DressLoan


@pytest.fixture()
def dress(db):
    return [
        mixer.blend('api.Dress'),
        mixer.blend('api.Dress'),
        mixer.blend('api.Dress')
    ]

@pytest.fixture()
def dressLoan(db):
    return [
        mixer.blend('api.DressLoan'),
        mixer.blend('api.DressLoan'),
        mixer.blend('api.DressLoan')
    ]

@pytest.fixture()
def group(db):
    return [
        mixer.blend('auth.Group', name="user"),
        mixer.blend('auth.Group', name="commessi")
    ]


def getClient(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def toJSON(obj):
    return json.dumps(model_to_dict(obj), default=str)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


def tests_dress_anon_user_get_nothing():
    path = reverse('dress-list')
    client = getClient()
    response = client.get(path, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')

def tests_dress_anon_user_cant_post():
    path = reverse('dress-list')
    client = getClient()
    response = client.post(path, {
        "brand": "ARMANIsss",
        "priceInCents": 5000,
        "material": "WOOL",
        "color": "BLACK",
        "size": 42
    }, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')

def tests_dress_anon_user_cant_put(dress):
    path = reverse('dress-detail', kwargs={'id': dress[0].id})
    client = getClient()
    response = client.put(path, {
        "startDate": "2022-12-17",
        "endDate": "2022-12-16",
        "dress": dress[0].id,
        "loaner": 2
    }, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')

def tests_dress_anon_user_cant_delete(dress):
    path = reverse('dress-detail', kwargs={'id': dress[0].id})
    client = getClient()
    response = client.delete(path, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')


def tests_dressLoan_anon_user_get_nothing():
    path = reverse('dressloan-list')
    client = getClient()
    response = client.get(path, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')

def tests_dressLoan_anon_user_cant_post():
    path = reverse('dressloan-list')
    client = getClient()
    response = client.post(path, {
        "startDate": "2022-12-05",
        "endDate": "2022-12-10",
        "dress": "fba6e9a1-1161-4b97-9a34-e474254bb0d8",
        "loaner": 2,
        "totalPrice": 700.0,
        "loanDurationDays": 7,
        "terminated": "false"
    }, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')

def tests_dressLoan_anon_user_cant_put(dressLoan):
    path = reverse('dressloan-detail', kwargs={'id': dressLoan[0].id})
    client = getClient()
    response = client.put(path, {
        "id": dressLoan[0].id,
        "startDate": "2022-12-05",
        "endDate": "2022-12-10",
        "dress": "fba6e9a1-1161-4b97-9a34-e474254bb0d8",
        "loaner": 2,
        "totalPrice": 700.0,
        "loanDurationDays": 7,
        "terminated": "false"
    }, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')

def tests_dressLoan_anon_user_cant_delete(dressLoan):
    path = reverse('dressloan-detail', kwargs={'id': dressLoan[0].id})
    client = getClient()
    response = client.delete(path, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')