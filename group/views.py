from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from user_service.permissions import IsAdminUser, CustomIsAuthenticated as IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_302_FOUND, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from group.serializers import GroupSerializer
from group.models import Group

from user_service.exceptions import GroupAlreadyExists, InvalidRequestData, GroupDoesNotExist


class GroupListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated & IsAdminUser]
    serializer_class = GroupSerializer

    def get_queryset(self):
        qs = Group.objects.filter(licence_id=self.request.user.licence_id)
        return qs

    def list(self, request, *args, **kwargs):
        groups = self.get_queryset()

        serializer = self.get_serializer_class()
        groups_to = serializer(groups, many=True)
        return Response(groups_to.data)

    def create(self, request, *args, **kwargs):
        form = request.data
        if not form:
            raise InvalidRequestData()

        form['licence_id'] = request.user.licence_id

        serializer = self.get_serializer_class()
        group = serializer(data=form)
        group.is_valid(raise_exception=True)
        try:
            group_instance = group.save()
        except IntegrityError as e:
            raise GroupAlreadyExists()

        return Response(group.validated_data)


class GroupDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & IsAdminUser]
    serializer_class = GroupSerializer

    def get_queryset(self):
        qs = Group.objects.filter(licence_id=self.request.user.licence_id)
        return qs

    def retrieve(self, request, *args, **kwargs):
        group = self.get_queryset().filter(name=self.kwargs['group_name'])
        if not group.exists():
            raise GroupDoesNotExist
        group = group.get()

        group_to = self.get_serializer_class()(group)

        return Response(group_to.data, status=HTTP_302_FOUND)

    def update(self, request, *args, **kwargs):
        group = self.get_queryset().filter(name=self.kwargs['group_name'])
        if not group.exists():
            raise GroupDoesNotExist()
        group = group.get()

        group_to = self.get_serializer_class()(group, data=request.data)
        group_to.is_valid(raise_exception=True)
        try:
            group_to.save()
        except IntegrityError as e:
            raise GroupAlreadyExists()

        return Response(group_to.data)

    def destroy(self, request, *args, **kwargs):
        group = self.get_queryset().filter(name=self.kwargs['group_name'])
        if not group.exists():
            raise GroupDoesNotExist()
        group = group.get()

        group.delete()

        return Response(status=HTTP_204_NO_CONTENT)
