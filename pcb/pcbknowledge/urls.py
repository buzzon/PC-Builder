from django.urls import path
from . import views

app_name = 'pcbknowledge'
urlpatterns = [
    path('', views.index, name='index'),
    path('questions', views.questions, name='questions')
]
