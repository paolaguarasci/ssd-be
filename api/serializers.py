from api.models import Dress, DressLoan
from rest_framework import serializers

class DressSerializers(serializers.ModelSerializer):
  class Meta:
    fields = "__all__"
    model = Dress


class DressLoanSerializers(serializers.ModelSerializer):

  #totalPrice = serializers.T

  class Meta:
    fields = "__all__"
    model = DressLoan