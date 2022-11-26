from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import (DjangoModelPermissions, IsAdminUser,
                                        IsAuthenticated)

from api.models import Dress, DressLoan
from api.serializers import (DressLoanSerializers, DressSerializers,
                             UserSerializer)


class DressList(generics.ListCreateAPIView):
    queryset = Dress.objects.all()
    serializer_class = DressSerializers
    permission_classes = [DjangoModelPermissions]
    lookup_field = "id"

class DressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dress.objects.all()
    serializer_class = DressSerializers
    lookup_field = "id"
    permission_classes = [DjangoModelPermissions]


class DressLoanList(generics.ListCreateAPIView):
    queryset = DressLoan.objects.all()
    serializer_class = DressLoanSerializers
    permission_classes = [DjangoModelPermissions]
    lookup_field = "id"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DressLoan.objects.all()
        return DressLoan.objects.filter(Q(insertBy=self.request.user) | Q(loaner=self.request.user))

    def perform_create(self, serializer):
        serializer.save(insertBy=self.request.user)


class DressLoanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DressLoan.objects.all()
    serializer_class = DressLoanSerializers
    lookup_field = "id"
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DressLoan.objects.all()
        return DressLoan.objects.filter(Q(insertBy=self.request.user) | Q(loaner=self.request.user))
        


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)