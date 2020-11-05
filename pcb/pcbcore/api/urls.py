from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'Brand', views.BrandViewSet)
router.register(r'Socket', views.SocketViewSet)
router.register(r'Chipset', views.ChipsetViewSet)
router.register(r'CPU', views.CPUViewSet)
router.register(r'GPU', views.GPUViewSet)
router.register(r'RAM', views.RAMViewSet)
router.register(r'MotherBoard', views.MotherBoardViewSet)
router.register(r'ROM', views.ROMViewSet)
router.register(r'PowerSupply', views.PowerSupplyViewSet)

app_name = 'pcbcore'
urlpatterns = [
    url('', include(router.urls)),
]
