from django.http import JsonResponse
from rest_framework import viewsets, permissions, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from pcbcore.api.serializers import *
from pcbcore.models import *


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def create(self, request, **kwargs):
        obj, created = Brand.objects.get_or_create(title=request.data.get("title"))
        serializer = BrandSerializer(obj)
        return JsonResponse(serializer.data)


class SocketViewSet(viewsets.ModelViewSet):
    queryset = Socket.objects.all()
    serializer_class = SocketSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def create(self, request, **kwargs):
        obj, created = Socket.objects.get_or_create(title=request.data.get("title"))
        serializer = SocketSerializer(obj)
        return JsonResponse(serializer.data)


class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class MemoryTypeViewSet(viewsets.ModelViewSet):
    queryset = MemoryType.objects.all()
    serializer_class = MemoryTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def create(self, request, **kwargs):
        obj, created = MemoryType.objects.get_or_create(title=request.data.get("title"))
        serializer = MemoryTypeSerializer(obj)
        return JsonResponse(serializer.data)


class RAMViewSet(viewsets.ModelViewSet):
    queryset = RAM.objects.all()
    serializer_class = RAMSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class FormfactorViewSet(viewsets.ModelViewSet):
    queryset = Formfactor.objects.all()
    serializer_class = FormfactorSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def create(self, request, **kwargs):
        obj, created = Formfactor.objects.get_or_create(title=request.data.get("title"))
        serializer = FormfactorSerializer(obj)
        return JsonResponse(serializer.data)


class ChipsetViewSet(viewsets.ModelViewSet):
    queryset = Chipset.objects.all()
    serializer_class = ChipsetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def create(self, request, **kwargs):
        obj, created = Chipset.objects.get_or_create(title=request.data.get("title"))
        serializer = ChipsetSerializer(obj)
        return JsonResponse(serializer.data)


class MotherBoardViewSet(viewsets.ModelViewSet):
    queryset = MotherBoard.objects.all()
    serializer_class = MotherBoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class SSDViewSet(viewsets.ModelViewSet):
    queryset = SSD.objects.all()
    serializer_class = SSDSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class HDDViewSet(viewsets.ModelViewSet):
    queryset = HDD.objects.all()
    serializer_class = HDDSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class PowerSupplyViewSet(viewsets.ModelViewSet):
    queryset = PowerSupply.objects.all()
    serializer_class = PowerSupplySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
