"""
URL configuration for DRFAuth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
import DRFAuth.views as views
from rest_framework.routers import DefaultRouter
from .views import LoginAPI, RegisterAPI,LogoutView, UserListView, UserDetailView, ProductListView ,StoreView, OrderView,AccessRuleView, api_root



urlpatterns = [
    path("", api_root, name='api-root'), 
    path('api/register/', RegisterAPI.as_view(), name="register"),
    path("api/login/", LoginAPI.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-details_edit'),
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/stores/', StoreView.as_view(), name='store-list'),
    path('api/orders/', OrderView.as_view(), name='order-list'),
    path('api/access/rules/', AccessRuleView.as_view(), name='access-rule-list'),
]