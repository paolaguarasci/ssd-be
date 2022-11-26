from django.urls import path

from api.apis import (DressDetail, DressList, DressLoanDetail, DressLoanList,
                      UserDetail, UserList)

urlpatterns = [
    path('dress/<uuid:id>', DressDetail.as_view()),
    path('dress/', DressList.as_view()),
    path('loan/<uuid:id>', DressLoanDetail.as_view()),
    path('loan/', DressLoanList.as_view()),
    path('user/', UserList.as_view()),
    path('user/<int:id>', UserDetail.as_view())
]

