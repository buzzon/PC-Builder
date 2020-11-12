from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_views

from . import views

router = DefaultRouter()
router.register(r'Brand', views.BrandViewSet)
router.register(r'Socket', views.SocketViewSet)
router.register(r'CPU', views.CPUViewSet)
router.register(r'GPU', views.GPUViewSet)
router.register(r'MemoryType', views.MemoryTypeViewSet)
router.register(r'RAM', views.RAMViewSet)
router.register(r'Formfactor', views.FormfactorViewSet)
router.register(r'Chipset', views.ChipsetViewSet)
router.register(r'MotherBoard', views.MotherBoardViewSet)
router.register(r'HDD', views.HDDViewSet)
router.register(r'SSD', views.SSDViewSet)
router.register(r'PowerSupply', views.PowerSupplyViewSet)

app_name = 'pcbcore-api'
urlpatterns = [
    url('', include(router.urls)),
    url(r'userRegistration/$', views.UserCreate.as_view(), name="user-registration"),
    url(r'getToken/$', rest_views.obtain_auth_token, name="get-token"),
]
