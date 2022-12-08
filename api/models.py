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
        self.deleted = True
        self.save()
 


def getTomorrow():
    return date.today()+timedelta(days=1)



class DressLoan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startDate = models.DateField(
        default=date.today, validators=[startDateValidator])
    endDate = models.DateField(default=getTomorrow)
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    loaner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='loans')
    insertBy = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='loansInsert')
    terminated = models.BooleanField(default=False)

    @property
    def totalPrice(self):
        totalPrice = self.dress.priceInCents * \
            (self.endDate - self.startDate).days
        return totalPrice / 100

    @property
    def loanDurationDays(self):
        return (self.endDate - self.startDate).days

    def _validate_start_end_dates(self):
        if self.endDate < self.startDate:
            raise ValidationError("End date cannot be before start date.")

    def save(self, *args, **kwargs):
        self._validate_start_end_dates()
        dress1 = Dress.objects.filter(id=self.dress.id)
        obj = DressLoan.objects.filter(Q(dress=dress1.first()) & Q(terminated=False))
        if len(obj) == 0:
            return super().save(*args, **kwargs)
        for loan in obj:
            if loan.id != self.id and (loan.startDate <= self.startDate and loan.endDate >= self.startDate):
                raise ValidationError("Dress already loan")
            elif loan.id != self.id and (loan.startDate <= self.endDate and loan.endDate >= self.endDate):
                raise ValidationError("Dress already loan")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.terminated = True
        self.save()