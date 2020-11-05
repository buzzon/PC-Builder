from rest_framework import viewsets, permissions

from pcbcore.api.serializers import *
from pcbcore.models import *


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class SocketViewSet(viewsets.ModelViewSet):
    queryset = Socket.objects.all()
    serializer_class = SocketSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChipsetViewSet(viewsets.ModelViewSet):
    queryset = Chipset.objects.all()
    serializer_class = ChipsetSerializer
    permission_classes = [permissions.IsAuthenticated]


class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer
    permission_classes = [permissions.IsAuthenticated]


class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = [permissions.IsAuthenticated]


class RAMViewSet(viewsets.ModelViewSet):
    queryset = RAM.objects.all()
    serializer_class = RAMSerializer
    permission_classes = [permissions.IsAuthenticated]


class MotherBoardViewSet(viewsets.ModelViewSet):
    queryset = MotherBoard.objects.all()
    serializer_class = MotherBoardSerializer
    permission_classes = [permissions.IsAuthenticated]


class ROMViewSet(viewsets.ModelViewSet):
    queryset = ROM.objects.all()
    serializer_class = ROMSerializer
    permission_classes = [permissions.IsAuthenticated]


class PowerSupplyViewSet(viewsets.ModelViewSet):
    queryset = PowerSupply.objects.all()
    serializer_class = PowerSupplySerializer
    permission_classes = [permissions.IsAuthenticated]
