from django.urls import path

from user.views import RegisterView, UsersListView, UserDetailsView, SetUserGroupsView, LogoutView, \
    SetUsersPasswordView, ResetPasswordView, CreateResetTokenView, ValidateResetTokenView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('register/', RegisterView.as_view(), name='user-register'),

    path('reset/', ResetPasswordView.as_view(), name='user-reset-password'),
    path('reset/token/', CreateResetTokenView.as_view(), name='user-reset-token'),
    path('reset/validate/', ValidateResetTokenView.as_view(), name='user-reset-validate'),

    path('', UsersListView.as_view(), name='user-list'),
    path('<int:user_id>/', UserDetailsView.as_view(), name='user-details'),
    path('<int:user_id>/password/', SetUsersPasswordView.as_view(), name='user-set-password'),
    path('<int:user_id>/permissions/', SetUserGroupsView.as_view(), name='user-permissions'),
]
