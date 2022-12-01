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
        fields = ['id', 'username', 'loans', 'loansInsert']


class DressSerializers(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'dressStatus', 'brand', 'priceInCents', 'material', 'color', 'size')
        model = Dress


class DressLoanSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'startDate', 'endDate', 'dress', 'loaner',
                  'totalPrice', 'loanDurationDays', 'insertBy')
        model = DressLoan
        # depth = 1

    # def create(self, validated_data):
    #     return DressLoan.objects.create(**validated_data)
