from django.contrib import admin
from .models import *


class TitleSearchAdmin(admin.ModelAdmin):
    search_fields = ['title']


class CPUAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'benchmark', 'price', 'get_url')
    list_filter = ['brand']
    search_fields = ['model']


class GPUAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'benchmark', 'price', 'get_url')
    list_filter = ['brand']
    search_fields = ['model']


class RAMAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'frequency', 'type', 'count', 'capacity', 'benchmark', 'price', 'get_url')
    list_filter = ['brand', 'capacity']
    search_fields = ['model']


class MotherBoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price', 'get_url')
    list_filter = ['brand']
    search_fields = ['model']


class ROMBoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price', 'get_url')
    list_filter = ['brand']
    search_fields = ['model']


class PowerSupplyBoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price', 'get_url')
    list_filter = ['brand']
    search_fields = ['model']


admin.site.register(Brand, TitleSearchAdmin)
admin.site.register(Socket, TitleSearchAdmin)
admin.site.register(CPU, CPUAdmin)
admin.site.register(GPU, GPUAdmin)
admin.site.register(MemoryType, TitleSearchAdmin)
admin.site.register(RAM, RAMAdmin)
admin.site.register(Formfactor, TitleSearchAdmin)
admin.site.register(Chipset, TitleSearchAdmin)
admin.site.register(MotherBoard, MotherBoardAdmin)
admin.site.register(ROM, ROMBoardAdmin)
admin.site.register(PowerSupply, PowerSupplyBoardAdmin)



