import os

from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

API_TITLE = "Dressy API"
API_DESCRIPTION = "A web API for creating and editing dress loans."


def index(request):
    context = {"title": API_TITLE, "description": API_DESCRIPTION}
    return render(request, 'api/index.html', context)


urlpatterns = [
    path('', index, name='index'),
    path(os.environ['SUPERUSER_PATH'], admin.site.urls),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('schema/', get_schema_view(title=API_TITLE)),
    path('api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/v1/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/', include('api.urls')),
]
