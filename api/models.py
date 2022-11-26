import uuid
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator, StepValueValidator)
from django.db import models

from api.validators import descriptionValidator, startDateValidator


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
    priceInCents = models.IntegerField(validators=[MinValueValidator(1000),
                                                   MaxValueValidator(1000000)])
    material = models.IntegerField(choices=MATERIALS)
    color = models.IntegerField(choices=COLORS)
    size = models.IntegerField(validators=[MinValueValidator(38),
                                           MaxValueValidator(60), StepValueValidator(2)])
    description = models.TextField(max_length=100, validators=[
                                   descriptionValidator, RegexValidator(r'^[A-Za-z0-9 .,_-]*$', message="Description must be write using allowed chars (A-Za-z0-9 .,_-)")])


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
        return super().save(*args, **kwargs)
