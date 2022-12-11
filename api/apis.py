from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.permissions import (DjangoModelPermissions, IsAdminUser,
                                        IsAuthenticated)
from rest_framework.response import Response

from api.models import Dress, DressLoan
from api.serializers import (DressLoanSerializers, DressSerializers,
                             UserSerializer)


def findIndex(key, enumerativ):
    for i in enumerativ:
        if i[1] == key:
            return i[0]


class DressList(generics.ListCreateAPIView):
    queryset = Dress.objects.all()
    serializer_class = DressSerializers
    permission_classes = [DjangoModelPermissions]
    lookup_field = "id"

    def get_queryset(self):
        userDB = User.objects.get(username=self.request.user)
        userGroupList = list(userDB.groups.values_list('name', flat=True))
        if self.request.user.is_superuser or "commessi" in userGroupList:
            return Dress.objects.all()
        return Dress.objects.filter(Q(deleted=False))

    def perform_create(self, serializer):
        brandIndex = findIndex(
            self.request.data['brandType'], Dress.BRANDS)

        if brandIndex == None:
            raise serializers.ValidationError(
                detail={'detail': "Brand is required"}, code=400)

        colorIndex = findIndex(
            self.request.data['colorType'], Dress.COLORS)

        if colorIndex == None:
            raise serializers.ValidationError(
                detail={'detail': "Color is required"}, code=400)

        materialIndex = findIndex(
            self.request.data['materialType'], Dress.MATERIALS)

        if materialIndex == None:
            raise serializers.ValidationError(
                detail={'detail': "Material is required"}, code=400)

        if serializer.is_valid():
            serializer.save(brand=brandIndex,
                            material=materialIndex, color=colorIndex)
            return super().perform_create(serializer)


class DressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dress.objects.all()
    serializer_class = DressSerializers
    lookup_field = "id"
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        userDB = User.objects.get(username=self.request.user)
        userGroupList = list(userDB.groups.values_list('name', flat=True))
        if self.request.user.is_superuser or "commessi" in userGroupList:
            return Dress.objects.all()
        return Dress.objects.filter(Q(deleted=False))

    def perform_update(self, serializer):
        brandIndex = findIndex(
            self.request.data['brandType'], Dress.BRANDS)

        if brandIndex == None:
            raise serializers.ValidationError(
                detail={'detail': "Brand is required"}, code=400)

        colorIndex = findIndex(
            self.request.data['colorType'], Dress.COLORS)

        if colorIndex == None:
            raise serializers.ValidationError(
                detail={'detail': "Color is required"}, code=400)

        materialIndex = findIndex(
            self.request.data['materialType'], Dress.MATERIALS)

        if materialIndex == None:
            raise serializers.ValidationError(
                detail={'detail': "Material is required"}, code=400)

        if serializer.is_valid():
            serializer.save(brand=brandIndex,
                            material=materialIndex, color=colorIndex)
            return super().perform_update(serializer)


class DressLoanList(generics.ListCreateAPIView):
    queryset = DressLoan.objects.all()
    serializer_class = DressLoanSerializers
    permission_classes = [DjangoModelPermissions]
    lookup_field = "id"

    def get_queryset(self):
        userDB = User.objects.get(username=self.request.user)
        userGroupList = list(userDB.groups.values_list('name', flat=True))
        if self.request.user.is_superuser or "commessi" in userGroupList:
            return DressLoan.objects.all()
        return DressLoan.objects.filter(Q(insertBy=self.request.user) | Q(loaner=self.request.user))

    def perform_create(self, serializer):
        userDB = User.objects.get(username=self.request.user)
        group = Group.objects.get(name="user")
        try:
            if (group in userDB.groups.all()):
                serializer.save(insertBy=self.request.user,
                                loaner=self.request.user)
            else:
                serializer.save(insertBy=self.request.user)
        except ValidationError as e:
            raise serializers.ValidationError({'detail': e.message}, code=400)


class DressLoanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DressLoan.objects.all()
    serializer_class = DressLoanSerializers
    lookup_field = "id"
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        userDB = User.objects.get(username=self.request.user)
        userGroupList = list(userDB.groups.values_list('name', flat=True))
        if self.request.user.is_superuser or "commessi" in userGroupList:
            return DressLoan.objects.all()
        return DressLoan.objects.filter(Q(loaner=self.request.user))


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
