from django.contrib import admin
from .models import *

admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(RAM)
admin.site.register(MotherBoard)
admin.site.register(ROM)
admin.site.register(PowerSupply)

admin.site.register(Brand)
admin.site.register(Socket)
admin.site.register(Chipset)
