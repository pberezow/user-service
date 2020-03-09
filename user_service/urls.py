"""user_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from .jwt_token import CustomTokenView as LoginView
from .jwt_token import CustomTokenRefreshView as RefreshTokenView
# from rest_framework_simplejwt.views import TokenRefreshSlidingView as RefreshTokenView
from user.views import FooView

prefix = ''

urlpatterns = [
    path('health/', FooView.as_view(), name='foo'),

    # JWT endpoints
    path(f'{prefix}login/', LoginView.as_view(), name='user-login'),
    path(f'{prefix}token/refresh/', RefreshTokenView.as_view(), name='user-token-refresh'),

    # user app endpoints
    path('', include('user.urls')),

    # group app endpoints
    path(f'{prefix}permissions/', include('group.urls')),
]


