from rest_framework.response import Response
from rest_framework.views import APIView


class PingPongView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request):
        return Response({'ping': 'pong'})
