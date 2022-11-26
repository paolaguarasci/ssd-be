import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer


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
    days = (dressLoan.endDate - dressLoan.startDate).days
    assert dressLoan.totalPrice == (days * dressLoan.dress.priceInCents) / 100

def test_loan_duration_must_be_equals_to_difference_beetwen_end_date_and_start_date(db):
    dressLoan = mixer.blend('api.DressLoan')
    days = (dressLoan.endDate - dressLoan.startDate).days
    assert dressLoan.loanDurationDays == days

    

# def test_dress_color_should_be_in_colors_enum(db):
#     with pytest.raises(ValidationError) as err:
#         dress = mixer.blend('api.Dress', color=)
#         dress.full_clean()
#     assert 'is less than or equal to 60' in '\n'.join(err.value.messages)

# def test_dress_author_should_be_valid_string(db):
#     with pytest.raises(ValidationError) as err:
#         dress = mixer.blend('api.Dress', author='sadASAS#$$#$%')
#         dress.full_clean()
#     assert 'Dress author must be a valid string' in '\n'.join(err.value.messages)

# def test_dress_author_of_lenght_0_raises_exception(db):
#     with pytest.raises(ValidationError) as err:
#         dress = mixer.blend('api.Dress', author='')
#         dress.full_clean()
#     assert 'This field cannot be blank' in '\n'.join(err.value.messages)


# def test_dress_year_blank_raises_exception(db):
#     with pytest.raises(ValidationError) as err:
#         dress = mixer.blend('api.Dress', year='')
#         dress.full_clean()
#     assert 'value must be an integer' in '\n'.join(err.value.messages)


# def test_dress_year_min_1200_raises_exception(db):
#     with pytest.raises(ValidationError) as err:
#         dress = mixer.blend('api.Dress', year=1199)
#         dress.full_clean()
#     assert 'greater than or equal to 1200' in '\n'.join(err.value.messages)


# def test_dress_year_over_2050_raises_exception(db):
#     with pytest.raises(ValidationError) as err:
#         dress = mixer.blend('api.Dress', year=2051)
#         dress.full_clean()
#     assert 'less than or equal to 2050' in '\n'.join(err.value.messages)

# def test_dressloan_loaner_should_a_valid_user(db):
#     with pytest.raises(ValidationError) as err:
#         dress = mixer.blend('api.DressLoan', loaner=1)
#         dress.full_clean()
#     print(err.value)
#     assert 'must be a "User" instance' in '\n'.join(err.value.messages)
