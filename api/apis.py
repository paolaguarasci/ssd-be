from django.shortcuts import render
from rest_framework import generics

from api.models import Dress, DressLoan
from api.serializers import DressLoanSerializers, DressSerializers


class DressList(generics.ListCreateAPIView):
  queryset=Dress.objects.all()
  serializer_class=DressSerializers

class DressDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset=Dress.objects.all()
  serializer_class=DressSerializers
  lookup_field="id"


class DressLoanList(generics.ListCreateAPIView):
  queryset=DressLoan.objects.all()
  serializer_class=DressLoanSerializers

class DressLoanDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset=DressLoan.objects.all()
  serializer_class=DressLoanSerializers
  lookup_field="id"