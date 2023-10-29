from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView


class PingPongView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        return Response({'ping': 'pong'})


def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'detail': 'This endpoint does not exist'
    }, status=404)


def custom500(request, exception=None):
    return JsonResponse({
        'status_code': 500,
        'detail': 'Mannaggia, we got 500 server error'
    }, status=500)
