from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from api.models import Dress, DressLoan


def getToday():
    return str(date.today())


def getTodayPlus(days):
    return str(date.today()+timedelta(days=days))


def test_dressLoan_terminate_false_by_default(db):
    d = mixer.blend('api.Dress')
    dressLoan = mixer.blend('api.DressLoan', dress=d)
    assert dressLoan.terminated == False


def test_dressLoan_terminate_true(db):
    dressLoan = mixer.blend('api.DressLoan')
    DressLoan.delete(dressLoan)
    assert dressLoan.terminated == True


def test_loans_start_date_must_not_be_in_the_past(db):
    with pytest.raises(ValidationError) as err:
        dressLoan = mixer.blend('api.DressLoan', startDate='2022-10-10')
        dressLoan.full_clean()
    assert 'Start date must not be in the past' in '\n'.join(
        err.value.messages)


def test_loans_end_date_must_be_after_start_date(db):
    with pytest.raises(ValidationError) as err:
        dressLoan = mixer.blend(
            'api.DressLoan', startDate='2022-12-10', endDate='2022-12-09')
        dressLoan.full_clean()
    assert 'End date cannot be before start date' in '\n'.join(
        err.value.messages)


def test_loans_total_price_must_be_equals_to_day_for_price(db):
    dressLoan = mixer.blend('api.DressLoan')
    dressLoan.full_clean()
    days = (dressLoan.endDate - dressLoan.startDate).days + 1
    assert dressLoan.totalPrice == (days * dressLoan.dress.priceInCents) // 100


def test_loan_duration_must_be_equals_to_difference_beetwen_end_date_and_start_date(db):
    dressLoan = mixer.blend('api.DressLoan')
    dressLoan.full_clean()
    days = (dressLoan.endDate - dressLoan.startDate).days + 1
    assert dressLoan.loanDurationDays == days


def test_try_to_loan_already_loaned_dress_same_period(db):
    dressLoan1 = mixer.blend(
        'api.DressLoan', startDate='2022-12-28', endDate='2022-12-30')
    with pytest.raises(ValidationError) as err:
        dressLoan2 = mixer.blend(
            'api.DressLoan', dress=dressLoan1.dress, startDate='2022-12-28', endDate='2022-12-30')
        dressLoan1.full_clean()
        dressLoan2.full_clean()
    assert 'Dress already loan' in '\n'.join(
        err.value.messages)


def test_try_to_loan_already_loaned_dress_overlap_startdate(db):
    dressLoan1 = mixer.blend(
        'api.DressLoan', startDate='2022-12-27', endDate='2022-12-30')
    with pytest.raises(ValidationError) as err:
        dressLoan2 = mixer.blend(
            'api.DressLoan', dress=dressLoan1.dress, startDate='2022-12-29', endDate='2023-01-31')
        dressLoan1.full_clean()
        dressLoan2.full_clean()
    assert 'Dress already loan' in '\n'.join(
        err.value.messages)


def test_try_to_loan_already_loaned_dress_overlap_enddate(db):
    dressLoan1 = mixer.blend(
        'api.DressLoan', startDate='2022-12-28', endDate='2022-12-31')
    with pytest.raises(ValidationError) as err:
        dressLoan2 = mixer.blend(
            'api.DressLoan', dress=dressLoan1.dress, startDate='2022-12-25', endDate='2022-12-29')
        dressLoan1.full_clean()
        dressLoan2.full_clean()
    assert 'Dress already loan' in '\n'.join(
        err.value.messages)


def test_try_to_loan_already_loaned_dress_no_overlap(db):
    dressLoan1 = mixer.blend(
        'api.DressLoan', startDate='2022-12-28', endDate='2022-12-31')
    dressLoan2 = mixer.blend(
        'api.DressLoan', dress=dressLoan1.dress, startDate='2023-12-07', endDate='2023-12-09')
    dressLoan1.full_clean()
    dressLoan2.full_clean()
    assert dressLoan1.id != dressLoan2.id


def test_try_to_loan_never_loaned(db):
    dressLoan = mixer.blend(
        'api.DressLoan', startDate=getToday(), endDate=getTodayPlus(1))
    dressLoan.full_clean()
    assert dressLoan.id


def test_try_to_update_whit_already_loan_dress(db):
    dress1 = mixer.blend('api.Dress')
    dress2 = mixer.blend('api.Dress')
    dressLoan1 = mixer.blend(
        'api.DressLoan', dress=dress1, startDate='2022-12-28', endDate='2022-12-31')
    dressLoan2 = mixer.blend(
        'api.DressLoan', dress=dress2, startDate='2022-12-28', endDate='2022-12-31')
    with pytest.raises(ValidationError) as err:
        dressLoan2.dress = dress1
        dressLoan2.save()
    assert 'Dress already loan' in '\n'.join(
        err.value.messages)

def test_try_to_loan_dress_deleted_rise_exception(db):
    dress = mixer.blend('api.Dress', deleted=True)
    with pytest.raises(ValidationError) as err:
        dressLoan = mixer.blend('api.DressLoan', dress=dress, startDate='2022-12-21', endDate='2022-12-23')
        dressLoan.full_clean()
        dress.full_clean()
    assert 'Dress unavailable' in '\n'.join(err.value.messages)