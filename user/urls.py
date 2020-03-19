from django.urls import path

from user.views import RegisterView
from user.views import UsersListView
from user.views import UserDetailsView
from user.views import SetUserGroupsView, SetUsersPasswordView, SetAvatarView
from user.views import LogoutView, CustomTokenView as LoginView, CustomTokenRefreshView as RefreshTokenView
from user.views import ResetPasswordView, CreateResetTokenView, ValidateResetTokenView
from user.views import HealthCheckView

urlpatterns = [
    # authenticationViews
    path('login/', LoginView.as_view(), name='user-login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='user-token-refresh'),
    path('logout/', LogoutView.as_view(), name='user-logout'),

    # registerUserView
    path('register/', RegisterView.as_view(), name='user-register'),

    # resetPasswordViews
    path('reset/', ResetPasswordView.as_view(), name='user-reset-password'),
    path('reset/token/', CreateResetTokenView.as_view(), name='user-reset-token'),
    path('reset/validate/', ValidateResetTokenView.as_view(), name='user-reset-validate'),

    # userListView
    path('', UsersListView.as_view(), name='user-list'),

    # userDetailsView
    path('<int:user_id>/', UserDetailsView.as_view(), name='user-details'),

    # userUpdateViews
    path('<int:user_id>/password/', SetUsersPasswordView.as_view(), name='user-set-password'),
    path('<int:user_id>/permissions/', SetUserGroupsView.as_view(), name='user-permissions'),
    path('<int:user_id>/avatar/', SetAvatarView.as_view(), name='user-set-avatar'),

    # otherUserViews
    path('health/', HealthCheckView.as_view(), name='foo'),
]

