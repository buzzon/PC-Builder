from django.contrib import admin
from .models import *


class TitleSearchAdmin(admin.ModelAdmin):
    search_fields = ['title']


class CPUAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'benchmark', 'price', 'cores', 'threads', 'socket', 'frequency',  'get_url')
    list_filter = ['brand']
    search_fields = ['model']


class GPUAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'benchmark', 'price', 'memory', 'get_url')
    list_filter = ['brand']
    search_fields = ['model']


class RAMAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'benchmark', 'price', 'type', 'frequency', 'count', 'capacity', 'get_url')
    list_filter = ['type', 'capacity']
    search_fields = ['model']


class MotherBoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price', 'formfactor', 'chipset', 'socket', 'year', 'get_url')
    list_filter = ['brand']
    search_fields = ['model']


class ROMBoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'benchmark', 'price', 'formfactor', 'capacity', 'get_url')
    list_filter = ['brand']
    search_fields = ['model']


class PowerSupplyBoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'power', 'price')
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
admin.site.register(SSD, ROMBoardAdmin)
admin.site.register(HDD, ROMBoardAdmin)
admin.site.register(PowerSupply, PowerSupplyBoardAdmin)



