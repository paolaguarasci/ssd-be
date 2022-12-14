from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Dress, DressLoan


class UserSerializer(serializers.ModelSerializer):
    loans = serializers.PrimaryKeyRelatedField(
        many=True, queryset=DressLoan.objects.all())
    loansInsert = serializers.PrimaryKeyRelatedField(
        many=True, queryset=DressLoan.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'loans', 'loansInsert', 'groups']


class DressSerializers(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'brandType', 'priceInCents', 'materialType',
                  'colorType', 'size', 'description', 'deleted')
        model = Dress
        read_only_fields = ['deleted']
    
    


class DressLoanSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'startDate', 'endDate', 'dress', 'loaner',
                  'totalPrice', 'loanDurationDays', 'insertBy', 'terminated')
        model = DressLoan
        read_only_fields = ['startDate','insertBy', 'terminated']
