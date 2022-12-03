import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from api.models import Dress, DressLoan


def tests_dress_description_should_be_at_most_100_chars_lenght(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', description='A'*101)
        dress.full_clean()
    assert 'at most 100 characters' in '\n'.join(err.value.messages)


def test_dress_description_should_be_at_last_1_char_lenght(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', description='')
        dress.full_clean()
    assert 'cannot be blank' in '\n'.join(err.value.messages)


def test_dress_description_should_be_valid_string(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend(
            'api.Dress', description='<script>alert(42);</script>')
        dress.full_clean()
    assert 'write using allowed chars' in '\n'.join(err.value.messages)


def test_dress_size_should_be_multiple_of_2(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', size='45')
        dress.full_clean()
    assert 'is a multiple of step size 2' in '\n'.join(err.value.messages)


def test_dress_size_should_be_at_least_38(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', size='36')
        dress.full_clean()
    assert 'is greater than or equal to 38' in '\n'.join(err.value.messages)


def test_dress_size_should_be_at_most_60(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', size='62')
        dress.full_clean()
    assert 'is less than or equal to 60' in '\n'.join(err.value.messages)

def test_dress_price_should_be_greter_than_1000(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', priceInCents=999)
        dress.full_clean()
    assert 'is greater than or equal to 1000' in '\n'.join(err.value.messages)

def test_dress_price_should_be_less_than_1000000(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', priceInCents=1000001)
        dress.full_clean()
    assert 'is less than or equal to 1000000' in '\n'.join(err.value.messages)


def test_dress_deleted_false_by_default(db):
    dress = mixer.blend('api.Dress')
    assert dress.deleted == False

def test_dress_deleted_true(db):
    dress = mixer.blend('api.Dress')
    Dress.delete(dress)
    assert dress.deleted == True

def test_dressLoan_terminate_false_by_default(db):
    d = mixer.blend('api.Dress')
    dressLoan = mixer.blend('api.DressLoan', dress=d)
    assert dressLoan.terminated == False

def test_dressLoan_terminate_true(db):
    dressLoan = mixer.blend('api.DressLoan')
    DressLoan.delete(dressLoan)
    assert dressLoan.terminated == True


def test_loans_start_date_must_be_in_present(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.DressLoan', startDate='2022-10-10')
        dress.full_clean()
    assert 'Start date must not be in the past' in '\n'.join(
        err.value.messages)


def test_loans_end_date_must_be_after_start_date(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend(
            'api.DressLoan', startDate='2022-12-10', endDate='2022-12-09')
        dress.full_clean()
    assert 'End date cannot be before start date' in '\n'.join(
        err.value.messages)


def test_loans_total_price_must_be_equals_to_day_for_price(db):
    dressLoan = mixer.blend('api.DressLoan')
    dressLoan.full_clean()
    days = (dressLoan.endDate - dressLoan.startDate).days
    assert dressLoan.totalPrice == (days * dressLoan.dress.priceInCents) / 100

def test_loan_duration_must_be_equals_to_difference_beetwen_end_date_and_start_date(db):
    dressLoan = mixer.blend('api.DressLoan')
    dressLoan.full_clean()
    days = (dressLoan.endDate - dressLoan.startDate).days
    assert dressLoan.loanDurationDays == days

def test_try_to_loan_alredy_loaned_dress_same_period(db):
    dressLoan1 = mixer.blend('api.DressLoan', startDate='2022-12-10', endDate='2022-12-12')
    with pytest.raises(ValidationError) as err:
        dressLoan2 = mixer.blend('api.DressLoan', dress=dressLoan1.dress, startDate='2022-12-10', endDate='2022-12-12')
        dressLoan1.full_clean()
        dressLoan2.full_clean()
    assert 'Vestito gia noleggiato' in '\n'.join(
        err.value.messages)


def test_try_to_loan_alredy_loaned_dress_overlap_startdate(db):
    dressLoan1 = mixer.blend('api.DressLoan', startDate='2022-12-10', endDate='2022-12-12')
    with pytest.raises(ValidationError) as err:
        dressLoan2 = mixer.blend('api.DressLoan', dress=dressLoan1.dress, startDate='2022-12-11', endDate='2022-12-14')
        dressLoan1.full_clean()
        dressLoan2.full_clean()
    assert 'Vestito gia noleggiato' in '\n'.join(
        err.value.messages)

def test_try_to_loan_alredy_loaned_dress_overlap_enddate(db):
    dressLoan1 = mixer.blend('api.DressLoan', startDate='2022-12-10', endDate='2022-12-12')
    with pytest.raises(ValidationError) as err:
        dressLoan2 = mixer.blend('api.DressLoan', dress=dressLoan1.dress, startDate='2022-12-07', endDate='2022-12-11')
        dressLoan1.full_clean()
        dressLoan2.full_clean()
    assert 'Vestito gia noleggiato' in '\n'.join(
        err.value.messages)

def test_try_to_loan_alredy_loaned_dress_no_overlap(db):
    dressLoan1 = mixer.blend('api.DressLoan', startDate='2022-12-10', endDate='2022-12-12')
    dressLoan2 = mixer.blend('api.DressLoan', dress=dressLoan1.dress, startDate='2022-12-7', endDate='2022-12-9')
    dressLoan1.full_clean()
    dressLoan2.full_clean()
    assert dressLoan1.id != dressLoan2.id

def test_try_to_loan_never_loaned(db):
    dressLoan = mixer.blend('api.DressLoan', startDate='2022-12-10', endDate='2022-12-12')
    dressLoan.full_clean()
    assert dressLoan.id 

def test_try_to_update_whit_alredy_loan_dress(db):
    dress1 = mixer.blend('api.Dress')
    dress2 = mixer.blend('api.Dress')
    dressLoan1 = mixer.blend('api.DressLoan', dress=dress1, startDate='2022-12-10', endDate='2022-12-12')
    dressLoan2 = mixer.blend('api.DressLoan', dress=dress2, startDate='2022-12-10', endDate='2022-12-12')
    with pytest.raises(ValidationError) as err:
        dressLoan2.dress = dress1
        dressLoan2.save()
    assert 'Vestito gia noleggiato' in '\n'.join(
        err.value.messages)
