import json

import pytest
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient

from api.models import Dress, DressLoan


@pytest.fixture()
def dress(db):
    return [mixer.blend('api.Dress'), mixer.blend('api.Dress'), mixer.blend('api.Dress')]


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


def tests_dressLoan_anon_user_get_nothing():
    path = reverse('dressloan-list')
    client = getClient()
    response = client.get(path, secure=True)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'credentials were not provided.')


def test_dress_user_get_list(dress):
    path = reverse('dress-list')
    user = mixer.blend(get_user_model())
    client = getClient(user)
    response = client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(dress)

def test_dress_retrive_a_single_dress(dress):
    path = reverse('dress-detail', kwargs={'id': dress[0].id})
    user = mixer.blend(get_user_model())
    client = getClient(user)
    response = client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert obj['id'] == str(dress[0].id)


def test_user_receives_a_list_with_only_his_loan(dress):
    path = reverse('dressloan-list')
    user = mixer.blend(get_user_model())
    userLoan = mixer.blend('api.DressLoan', loaner=user)
    client = getClient(user)
    response = client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == 1
    assert obj[0]['loaner'] == user.id


def test_user_cant_update_his_loan(dress):
    user = mixer.blend(get_user_model())
    userLoan = mixer.blend('api.DressLoan', loaner=user)
    client = getClient(user)
    path = reverse('dressloan-detail', kwargs={'id': userLoan.id})
    res = client.get(path, secure=True)
    obj = parse(res)
    obj['endDate'] = "2022-12-10"
    path = reverse('dressloan-detail', kwargs={'id': userLoan.id})
    response = client.put(path, obj, secure=True)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_cant_delete_his_loan(dress):
    user = mixer.blend(get_user_model())
    userLoan = mixer.blend('api.DressLoan', loaner=user)
    client = getClient(user)
    path = reverse('dressloan-detail', kwargs={'id': userLoan.id})
    response = client.delete(path, secure=True)
    assert response.status_code == HTTP_403_FORBIDDEN
