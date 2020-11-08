from django.conf.urls import url

from . import views

app_name = 'pcbknowledge'
urlpatterns = [
    url('', views.index, name='index')
]
