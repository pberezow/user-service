from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class HealthCheckView(ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response({'status': 'UP'})
