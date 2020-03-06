from django.urls import path, include
from .views import GroupViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', GroupViewSet, 'test')

urlpatterns = [
    path('', include(router.urls), name='test'),

]
