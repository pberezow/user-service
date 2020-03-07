from django.urls import path

from user.views import RegisterView, UsersListView, UserDetailsView, SetUserGroupsView, LogoutView, SetUsersPasswordView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('', UsersListView.as_view(), name='user-list'),
    path('<int:user_id>/', UserDetailsView.as_view(), name='user-details'),
    path('<int:user_id>/password/', SetUsersPasswordView.as_view(), name='user-set-password'),
    path('<int:user_id>/permissions/', SetUserGroupsView.as_view(), name='user-permissions'),
]
