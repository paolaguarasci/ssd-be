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

def test_dress_price_in_cents_should_be_greter_or_equal_than_1000(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', priceInCents=999)
        dress.full_clean()
    assert 'is greater than or equal to 1000' in '\n'.join(err.value.messages)

def test_dress_price_in_cents_should_be_less_or_equal_than_1000000(db):
    with pytest.raises(ValidationError) as err:
        dress = mixer.blend('api.Dress', priceInCents=1000001)
        dress.full_clean()
    assert 'is less than or equal to 1000000' in '\n'.join(err.value.messages)

def test_dress_material_must_be_present_in_materials_list(db):
    dress = mixer.blend('api.Dress')
    check = False
    for material in Dress.MATERIALS:
        if dress.material in material:
            check = True
            break
    assert check

def test_dress_brand_must_be_present_in_brands_list(db):
    dress = mixer.blend('api.Dress')
    check = False
    for brand in Dress.BRANDS:
        if dress.brand in brand:
            check = True
            break
    assert check

def test_dress_color_must_be_present_in_colors_list(db):
    dress = mixer.blend('api.Dress')
    check = False
    for color in Dress.COLORS:
        if dress.color in color:
            check = True
            break
    assert check

def test_dress_deleted_false_by_default(db):
    dress = mixer.blend('api.Dress')
    assert dress.deleted == False

def test_dress_deleted_true(db):
    dress = mixer.blend('api.Dress')
    Dress.delete(dress)
    assert dress.deleted == True