from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.contrib.auth import get_user_model

import uuid
# Create your models here.



class Dress(models.Model):
    materials = (
      (0, "WOOL"),
      (1, 'SILK'),
      (2, 'COTTON'))
    brands = (
      (0, 'GUCCI'),
      (1, 'ARMANI'),
      (2, 'VALENTINO')
    )

    colors = (
      (0, 'BLACK'),
      (1, 'BLUE'),
      (2, 'WHITE'),
      (3, 'RED'),
      (4, 'PINK'),
      (5, 'GRAY')
    )


    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    brand = models.IntegerField(choices=brands)
    priceInCents = models.IntegerField(validators=[MinValueValidator(0),
                                           MaxValueValidator(1000000)])
    material = models.IntegerField(choices=materials)
    color = models.IntegerField(choices=colors)
    size = models.IntegerField(validators=[MinValueValidator(38),
                                           MaxValueValidator(60)])
    
    def __str__(self):

      return str(self.id) + " | " + str(self.brands[self.brand][1]) + " | " + str(self.priceInCents / 100) + " | " + str(self.materials[self.material][1]) + " | " + str(self.colors[self.color][1]) + " | " + str(self.size)
    



class DressLoan(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    startDate = models.DateField()
    endDate = models.DateField()
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @property
    def totalPrice(self):
      myDress = Dress.objects.get(pk=self.dress.id)
      totalPrice = myDress.priceInCents * (self.endDate - self.startDate).days
      return totalPrice /100 

    def __str__(self):
      return str(self.id) + " | " + str(self.startDate) + " | " + str(self.endDate) + " | " + str(self.dress.id) + " | " + str(self.user.username) + " | " + str(self.totalPrice)