import json
import os
from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.forms.models import model_to_dict
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST,
                                   HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND)
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
    user = User.objects.get(username=os.environ['STAFF_USERNAME'])
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    print("refresh.access_token", refresh.access_token)
    return client


def getToday():
    return str(date.today())


def getTodayPlus(days):
    return str(date.today()+timedelta(days=days))

######################### Dress    #############################################


@pytest.mark.django_db
def test_dress_commesso_get_all_list(api_client):
    path = reverse('dress-list')
    dress = Dress.objects.all()
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(dress)


@pytest.mark.django_db
def test_dress_commesso_get_single_item(api_client):
    dressLoanID = '28bce53b-6c7e-478b-ab85-a5f2066a5278'
    path = reverse('dress-detail', kwargs={'id': dressLoanID})
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert contains(response, 'id', dressLoanID)


@pytest.mark.django_db
def tests_dress_commesso_can_post(api_client):
    path = reverse('dress-list')
    response = api_client.post(path, {
        "brandType": "ARMANI",
        "priceInCents": 1234,
        "materialType": "WOOL",
        "colorType": "BLACK",
        "size": 42,
        "description": "Ciao"
    }, secure=True)
    print(response.data)
    assert response.status_code == HTTP_201_CREATED
    assert contains(response, 'brandType',
                    'ARMANI')

@pytest.mark.django_db
def tests_dress_commesso_can_post_but_wrong_data(api_client):
    path = reverse('dress-list')
    response = api_client.post(path, {
        "brandType": "ARMANIaaa",
        "priceInCents": 1234,
        "materialType": "WOOLsss",
        "colorType": "BLACKsss",
        "size": 42,
        "description": "Ciao"
    }, secure=True)
    print(response.data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert contains(response, 'detail',
                    'NOT NULL constraint failed')

@pytest.mark.django_db
def tests_dress_commesso_can_put(api_client):
    dressID = '28bce53b-6c7e-478b-ab85-a5f2066a5278'
    path = reverse('dress-detail', kwargs={'id': dressID})
    response = api_client.put(path, {
        "id": "28bce53b-6c7e-478b-ab85-a5f2066a5278",
        "brandType": "ARMANI",
        "priceInCents": 1234,
        "materialType": "WOOL",
        "colorType": "BLACK",
        "size": 42,
        "description": "Ciao"
    }, secure=True)
    assert response.status_code == HTTP_200_OK
    assert contains(response, 'brandType',
                    'ARMANI')


@pytest.mark.django_db
def tests_dress_commesso_can_delete(api_client):
    dressID = '28bce53b-6c7e-478b-ab85-a5f2066a5278'
    path = reverse('dress-detail', kwargs={'id': dressID})
    response = api_client.delete(path, secure=True)
    assert response.status_code == HTTP_204_NO_CONTENT

######################### Dress Loan #############################################


@pytest.mark.django_db
def test_dress_loan_commesso_get_all_list(api_client):
    path = reverse('dressloan-list')
    dressLoan = DressLoan.objects.all()
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(dressLoan)


@pytest.mark.django_db
def test_dress_loan_commesso_get_single_item(api_client):
    dressLoans = DressLoan.objects.all()
    dressLoanID = dressLoans[0].id
    path = reverse('dressloan-detail', kwargs={'id': dressLoanID})
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert contains(response, 'id', str(dressLoanID))


@pytest.mark.django_db
def tests_dress_loan_commesso_can_post(api_client):
    path = reverse('dressloan-list')
    response = api_client.post(path, {
        "startDate": getToday(),
        "endDate": getTodayPlus(5),
        "dress": "fba6e9a1-1161-4b97-9a34-e474254bb0d8",
        "loaner": 2
    }, secure=True)
    print(response.data)
    assert response.status_code == HTTP_201_CREATED
    assert contains(response, 'startDate', getToday())


@pytest.mark.django_db
def tests_dress_loan_commesso_can_put(api_client):
    dressLoans = DressLoan.objects.all()
    dressLoanID = dressLoans[0].id
    path = reverse('dressloan-detail', kwargs={'id': dressLoanID})
    response = api_client.put(path, {
        "startDate": getToday(),
        "endDate": getTodayPlus(5),
        "dress": "fba6e9a1-1161-4b97-9a34-e474254bb0d8",
        "loaner": 2,
        "totalPrice": 700.0,
        "loanDurationDays": 7,
        "terminated": "false"
    }, secure=True)
    assert response.status_code == HTTP_200_OK
    assert contains(response, 'startDate', getToday())


@pytest.mark.django_db
def tests_dress_loan_commesso_can_delete(api_client):
    dressLoans = DressLoan.objects.all()
    dressLoanID = dressLoans[0].id
    path = reverse('dressloan-detail', kwargs={'id': dressLoanID})
    response = api_client.delete(path, secure=True)
    assert response.status_code == HTTP_204_NO_CONTENT


######################### Users               #############################################

@pytest.mark.django_db
def test_user_commesso_cant_get_users_list(api_client):
    user = User.objects.get(username=os.environ['STAFF_USERNAME'])
    users = User.objects.all()
    path = reverse('user-list')
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_commesso_get_yours(api_client):
    user = User.objects.get(username=os.environ['STAFF_USERNAME'])
    path = reverse('user-detail', kwargs={'id': user.id})
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_200_OK
    assert contains(response, 'username', user.username)


@pytest.mark.django_db
def test_user_commesso_get_only_yours(api_client):
    user = User.objects.get(username=os.environ['USER_USERNAME'])
    path = reverse('user-detail', kwargs={'id': user.id})
    response = api_client.get(path, secure=True)
    assert response.status_code == HTTP_404_NOT_FOUND
