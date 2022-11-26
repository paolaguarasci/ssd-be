import uuid

from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class Dress(models.Model):

    materials = (
        (0, "WOOL"),
        (1, 'SILK'),
        (2, 'COTTON'))

    brands = (
        (0, 'GUCCI'),
        (1, 'ARMANI'),
        (2, 'VALENTINO'))

    colors = (
        (0, 'BLACK'),
        (1, 'BLUE'),
        (2, 'WHITE'),
        (3, 'RED'),
        (4, 'PINK'),
        (5, 'GRAY'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.IntegerField(choices=brands)
    priceInCents = models.IntegerField(validators=[MinValueValidator(1000),
                                                   MaxValueValidator(1000000)])
    material = models.IntegerField(choices=materials)
    color = models.IntegerField(choices=colors)
    size = models.IntegerField(validators=[MinValueValidator(38),
                                           MaxValueValidator(60)])


class DressLoan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startDate = models.DateField()
    endDate = models.DateField()
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    loaner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='loans')
    insertBy = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='loansInsert')

    @property
    def totalPrice(self):
        totalPrice = self.dress.priceInCents * \
            (self.endDate - self.startDate).days
        return totalPrice / 100

    @property
    def loanDurationDays(self):
        return (self.endDate - self.startDate).days
