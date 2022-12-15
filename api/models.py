import uuid
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator, StepValueValidator)
from django.db import models
from django.db.models import Q

from api.validators import descriptionSizeValidator, startDateValidator

MIN_SIZE = 38
MAX_SIZE = 60
MAX_CHARS_FIELD_LEN = 15
MIN_PRICE_IN_CENT = 1000
MAX_PRICE_IN_CENT = 1000000
REGEX_DESCRIPTION = "^[A-Za-z0-9 .,_-]*$"
ERROR_DESCRIPTION_CHARAPTER_NOT_ALLOWED = "Description must be write using allowed chars (A-Za-z0-9 .,_-)"
ERROR_DESCRIPTION_ENDDATE_BEFORE_STARTDATE = "End date cannot be before start date."
ERROR_DRESS_UNAVALIABLE = "Dress unavailable"
ERROR_DATE_IS_BEFORE_TODAY = "Start date must not be in the past"





class Dress(models.Model):
    MATERIALS = (
        (0, 'WOOL'),
        (1, 'SILK'),
        (2, 'COTTON'))

    BRANDS = (
        (0, 'GUCCI'),
        (1, 'ARMANI'),
        (2, 'VALENTINO'))

    COLORS = (
        (0, 'BLACK'),
        (1, 'BLUE'),
        (2, 'WHITE'),
        (3, 'RED'),
        (4, 'PINK'),
        (5, 'GRAY'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.IntegerField(choices=BRANDS)
    priceInCents = models.IntegerField(validators=[MinValueValidator(MIN_PRICE_IN_CENT),
                                                   MaxValueValidator(MAX_PRICE_IN_CENT)])
    material = models.IntegerField(choices=MATERIALS)
    color = models.IntegerField(choices=COLORS)
    size = models.IntegerField(validators=[MinValueValidator(MIN_SIZE),
                                           MaxValueValidator(MAX_SIZE), StepValueValidator(2)])
    description = models.TextField(max_length=100, validators=[
                                   descriptionSizeValidator, RegexValidator(f'{REGEX_DESCRIPTION}', message=f"{ERROR_DESCRIPTION_CHARAPTER_NOT_ALLOWED}")])
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.id:
            oldDress = Dress.objects.filter(id=self.id)
            if len(oldDress) == 1 and oldDress[0].deleted:
                raise ValidationError("Dress is already deleted")
        return super().save(*args, **kwargs)

    @property
    def brandType(self):
        return self.BRANDS[self.brand][1]

    @property
    def materialType(self):
        return self.MATERIALS[self.material][1]

    @property
    def colorType(self):
        return self.COLORS[self.color][1]

    def delete(self, *args, **kwargs):
        if self.deleted != True:
            self.deleted = True
            dressLoandLinked = DressLoan.objects.filter(dress=self)
            for l in dressLoandLinked:
                l.terminated = True
                l.save()
            self.save()


def getTomorrow():
    return date.today()+timedelta(days=1)


class DressLoan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startDate = models.DateField(
        default=date.today, validators=[])
    endDate = models.DateField(default=getTomorrow)
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE, validators=[
                              ])
    loaner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='loans')
    insertBy = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='loansInsert')
    terminated = models.BooleanField(default=False)

    @property
    def totalPrice(self):
        totalPrice = self.dress.priceInCents * \
            ((self.endDate - self.startDate).days + 1)
        return totalPrice // 100

    @property
    def loanDurationDays(self):
        return (self.endDate - self.startDate).days + 1

    def _validate_start_end_dates(self):
        if self.endDate < self.startDate:
            raise ValidationError("End date cannot be before start date.")

    def _startDateValidator(value) -> None:
        if value.startDate < date.today():
            raise ValidationError(f"{ERROR_DATE_IS_BEFORE_TODAY}")

    def _checkOverlapDate(value) -> None:
        print("Controllo overlap")
        dress1 = Dress.objects.filter(id=value.dress.id)
        objs = DressLoan.objects.filter(
            Q(dress=dress1.first()) & Q(terminated=False))
        newSD = value.startDate
        newED = value.endDate
        if len(objs) >= 1:
            for loan in objs:
                existSD = loan.startDate
                existED = loan.endDate
                if loan.id != value.id and ((newSD <= existSD and existSD <= newED)):
                    print("1")
                    raise ValidationError("Dress already loan")
                if loan.id != value.id and ((newSD <= existED and existED <= newED)):
                    print("2")
                    raise ValidationError("Dress already loan")
                if loan.id != value.id and ((newSD >= existSD and newED <= existED)):
                    print("3")
                    raise ValidationError("Dress already loan")

    def _dressDeletes(value) -> None:
        dress1 = Dress.objects.filter(id=value.dress.id)
        if (dress1[0].deleted):
            raise ValidationError(
                "You cannot change the loan because the dress is no longer available")
    
    def _validatorDressToLoan(value) -> None:
        if value.dress.deleted:
            raise ValidationError(ERROR_DRESS_UNAVALIABLE)

    def save(self, *args, **kwargs):
        oldDressLoan = DressLoan.objects.filter(id=self.id)
        print("ciao")
        if len(oldDressLoan) == 1 and oldDressLoan[0].terminated:
            print("ciao")
            raise ValidationError("DressLoan is already terminated")

        elif len(oldDressLoan) == 1:
            self._validate_start_end_dates()
            self._dressDeletes()
            self._checkOverlapDate()
            self.startDate = oldDressLoan[0].startDate
            return super().save(*args, **kwargs)

        elif len(oldDressLoan) == 0:
            self._validatorDressToLoan()
            self._validate_start_end_dates()
            self._startDateValidator()
            self._dressDeletes()
            self._checkOverlapDate()
            return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if (self.terminated == False):
            self.terminated = True
            self.save()
