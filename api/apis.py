from django.shortcuts import render
from rest_framework import generics
from api.models import Dress, DressLoan
from api.serializers import DressSerializers, DressLoanSerializers
# Create your views here.

class DressList(generics.ListCreateAPIView):
  queryset=Dress.objects.all()
  serializer_class=DressSerializers

class DressDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset=Dress.objects.all()
  serializer_class=DressSerializers


class DressLoanList(generics.ListCreateAPIView):
  queryset=DressLoan.objects.all()
  serializer_class=DressLoanSerializers

class DressLoanDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset=DressLoan.objects.all()
  serializer_class=DressLoanSerializers