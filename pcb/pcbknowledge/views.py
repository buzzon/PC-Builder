from django.shortcuts import render

from pcbcore.models import *


def index(request):
    brand_count = Brand.objects.count()
    socket_count = Socket.objects.count()
    cpu_count = CPU.objects.count()
    gpu_count = GPU.objects.count()
    memory_type_count = MemoryType.objects.count()
    ram_count = RAM.objects.count()
    formfactor_count = Formfactor.objects.count()
    chipset_count = Chipset.objects.count()
    mother_board_count = MotherBoard.objects.count()
    ssd_count = SSD.objects.count()
    hdd_count = HDD.objects.count()
    power_supply_count = PowerSupply.objects.count()

    return render(
        request,
        'index.html',
        context={
            'brand_count': brand_count,
            'socket_count': socket_count,
            'cpu_count': cpu_count,
            'gpu_count': gpu_count,
            'memory_type_count': memory_type_count,
            'ram_count': ram_count,
            'formfactor_count': formfactor_count,
            'chipset_count': chipset_count,
            'mother_board_count': mother_board_count,
            'ssd_count': ssd_count,
            'hdd_count': hdd_count,
            'power_supply_count': power_supply_count,
        }
    )
