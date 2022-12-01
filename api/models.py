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
        ('WOOL', 'WOOL'),
        ('SILK', 'SILK'),
        ('COTTON', 'COTTON'))

    BRANDS = (
        ('GUCCI', 'GUCCI'),
        ('ARMANI', 'ARMANI'),
        ('VALENTINO', 'VALENTINO'))

    COLORS = (
        ('BLACK', 'BLACK'),
        ('BLUE', 'BLUE'),
        ('WHITE', 'WHITE'),
        ('RED', 'RED'),
        ('PINK', 'PINK'),
        ('GRAY', 'GRAY'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(choices=BRANDS, max_length = 15)
    priceInCents = models.IntegerField(validators=[MinValueValidator(1000),
                                                   MaxValueValidator(1000000)])
    material = models.CharField(choices=MATERIALS, max_length = 15)
    color = models.CharField(choices=COLORS, max_length = 15)
    size = models.IntegerField(validators=[MinValueValidator(38),
                                           MaxValueValidator(60), StepValueValidator(2)])
    description = models.TextField(max_length=100, validators=[
                                   descriptionValidator, RegexValidator(r'^[A-Za-z0-9 .,_-]*$', message="Description must be write using allowed chars (A-Za-z0-9 .,_-)")])
    dressStatus = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.dressStatus = False
        self.save()
        #super(Dress, self).delete(*args, **kwargs)




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


# class DressStatus():
#     available = False

#     def setAvailable(self):
#         self.available = True
#     def setUnAvailable(self):
#         self.available = False