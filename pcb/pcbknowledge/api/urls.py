from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'Questions', views.QuestionViewSet)

app_name = 'pcbknowledge-api'
urlpatterns = [
    url('', include(router.urls)),
    url('clear_question', views.clear_question, name='clear_question')
]
