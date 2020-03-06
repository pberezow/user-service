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
from rest_framework_simplejwt.views import TokenRefreshSlidingView as RefreshTokenView
from user.views import RegisterView, UsersListView, UserDetailsView, SetUserGroupsView, LogoutView, SetUsersPasswordView, FooView
from group.views import GroupDetailsView, GroupListCreateView

prefix = ''

urlpatterns = [
    path('health/', FooView.as_view(), name='foo'),
    # JWT endpoints
    path(f'{prefix}login/', LoginView.as_view(), name='user-login'),
    path(f'{prefix}token/refresh/', RefreshTokenView.as_view(), name='user-token-refresh'),
    # user app endpoints
    path(f'{prefix}logout/', LogoutView.as_view(), name='user-logout'),
    path(f'{prefix}register/', RegisterView.as_view(), name='user-register'),
    path(f'{prefix}', UsersListView.as_view(), name='user-list'),
    path(f'{prefix}<int:user_id>/', UserDetailsView.as_view(), name='user-details'),
    path(f'{prefix}<int:user_id>/password/', SetUsersPasswordView.as_view(), name='user-set-password'),
    path(f'{prefix}<int:user_id>/permissions/', SetUserGroupsView.as_view(), name='user-permissions'),
    # group app endpoints
    path(f'{prefix}permissions/', GroupListCreateView.as_view(), name='group-list-create'),
    path(f'{prefix}permissions/<str:group_name>/', GroupDetailsView.as_view(), name='group-details'),

    path('admin/', admin.site.urls),
]
