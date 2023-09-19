"""planfit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from projects.api import CustomTokenObtainPairView, EntrenamientoListCreateView, EntrenamientoRetrieveUpdateDeleteView, PersonalDataListCreateView, PersonalDataRetrieveUpdateDeleteView, PlanListCreateView, PlanRetrieveUpdateDeleteView, UserCreateView, UserRetrieveUpdateDeleteView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("projects.urls")),
    path("users/", UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/", UserRetrieveUpdateDeleteView.as_view(), name="user-detail"),
    path(
        "entrenamientos/",
        EntrenamientoListCreateView.as_view(),
        name="entrenamiento-list",
    ),
    path(
        "entrenamientos/<int:pk>/",
        EntrenamientoRetrieveUpdateDeleteView.as_view(),
        name="entrenamiento-detail",
    ),
    path(
        "planes/",
        PlanListCreateView.as_view(),
        name="planes-list",
    ),
    path(
        "planes/<int:pk>/",
        PlanRetrieveUpdateDeleteView.as_view(),
        name="planes-detail",
    ),
    path(
        "personal-data/",
        PersonalDataListCreateView.as_view(),
        name="personal-data-list",
    ),
    path(
        "personal-data/<int:pk>/",
        PersonalDataRetrieveUpdateDeleteView.as_view(),
        name="personal-data-detail",
    ),
    path("token/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
