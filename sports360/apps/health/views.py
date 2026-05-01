from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import django


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'Sports360 API is running',
            'django_version': django.get_version(),
        })
