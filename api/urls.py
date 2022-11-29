from django.urls import path

from api.apis import (DressDetail, DressList, DressLoanDetail, DressLoanList,
                      UserDetail, UserList)





urlpatterns = [
    path('dress/<uuid:id>', DressDetail.as_view(), name='dress-detail'),
    path('dress/', DressList.as_view(), name='dress-list'),
    path('loan/<uuid:id>', DressLoanDetail.as_view(), name='dressloan-detail'),
    path('loan/', DressLoanList.as_view(), name='dressloan-list'),
    path('user/', UserList.as_view(), name='user-list'),
    path('user/<int:id>', UserDetail.as_view(), name='user-detail')
]

