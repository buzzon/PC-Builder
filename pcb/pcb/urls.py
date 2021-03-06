"""pcb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pcbknowledge.admin import expert

urlpatterns = [
    path(r'', include('pcbknowledge.urls')),
    path(r'api/core/', include('pcbcore.api.urls')),
    path(r'api/knowledge/', include('pcbknowledge.api.urls')),
    path(r'admin/', admin.site.urls, name="admin"),
    path(r'expert/', expert.urls),
    path(r'api-auth/', include('rest_framework.urls')),
]
