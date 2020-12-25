from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from pcbknowledge.api.serializers import *
from pcbknowledge.models import *


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
