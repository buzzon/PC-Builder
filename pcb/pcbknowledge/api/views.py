from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAdminUser

from pcbknowledge.api.serializers import *
from pcbknowledge.models import *


def index(request):
    return HttpResponse("Welcome to the expert system to build a PC")


@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([SessionAuthentication])
def clear_question(request):
    Question.objects.all().delete()
    return HttpResponse("Пизда рулям, мы просрали базу знаний :с")


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
