from django.urls import path

from api.apis import DressList, DressDetail, DressLoanList, DressLoanDetail

urlpatterns = [
    path('dress/<int:id>', DressDetail.as_view()),
    path('dress/', DressList.as_view()),
    path('loan/<int:id>', DressLoanDetail.as_view()),
    path('loan/', DressLoanList.as_view())
]