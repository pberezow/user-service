from django.urls import path

from group.views import GroupDetailsView, GroupListCreateView


urlpatterns = [
    path('', GroupListCreateView.as_view(), name='group-list-create'),
    path('<str:group_name>/', GroupDetailsView.as_view(), name='group-details'),
]
