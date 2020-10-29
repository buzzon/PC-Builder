from pcbcore.models import *


class Component(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Factor(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    coefficient = models.IntegerField()
    essence = models.ForeignKey('Essence', on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.coefficient}] {self.component}'


class Essence(models.Model):
    title = models.CharField(max_length=256)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    next_question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='next_question')

    def __str__(self):
        return self.title


class Question(models.Model):
    MEDIA_CHOICES = [
        ('CPU', (
            ('CPU_title', 'CPU title'),
            ('CPU_brand', 'CPU brand'),
            ('CPU_cores', 'CPU cores'),
            ('CPU_threads', 'CPU threads'),
            ('CPU_frequency', 'CPU frequency'),
            ('CPU_socket', 'CPU socket'),
            ('CPU_value', 'CPU value'),
            ('CPU_price', 'CPU price'),
        )),
        ('GPU', (
            ('GPU_title', 'GPU title'),
            ('GPU_brand', 'GPU brand'),
            ('GPU_memory', 'GPU memory'),
            ('GPU_value', 'GPU value'),
            ('GPU_price', 'GPU price'),
        )),
        ('MotherBoard', (
            ('MotherBoard_title', 'MotherBoard title'),
            ('MotherBoard_brand', 'MotherBoard brand'),
            ('MotherBoard_chipset', 'MotherBoard chipset'),
            ('MotherBoard_socket', 'MotherBoard socket'),
            ('MotherBoard_value', 'MotherBoard value'),
            ('MotherBoard_price', 'MotherBoard price'),
        )),
        ('RAM', (
            ('RAM_title', 'RAM title'),
            ('RAM_brand', 'RAM brand'),
            ('RAM_frequency', 'RAM frequency'),
            ('RAM_size', 'RAM size'),
            ('RAM_value', 'RAM value'),
            ('RAM_price', 'RAM price'),
        )),
        ('HDD', (
            ('HDD_title', 'HDD title'),
            ('HDD_brand', 'HDD brand'),
            ('HDD_type', 'HDD type'),
            ('HDD_read', 'HDD read'),
            ('HDD_write', 'HDD write'),
            ('HDD_size', 'HDD size'),
            ('HDD_value', 'HDD value'),
            ('HDD_price', 'HDD price'),
        )),
        ('SSD', (
            ('SSD_title', 'SSD title'),
            ('SSD_brand', 'SSD brand'),
            ('SSD_type', 'SSD type'),
            ('SSD_read', 'SSD read'),
            ('SSD_write', 'SSD write'),
            ('SSD_size', 'SSD size'),
            ('SSD_value', 'SSD value'),
            ('SSD_price', 'SSD price'),
        )),
        ('PowerSupply', (
            ('PowerSupply_title', 'PowerSupply title'),
            ('PowerSupply_brand', 'PowerSupply brand'),
            ('PowerSupply_power', 'PowerSupply power'),
            ('PowerSupply_value', 'PowerSupply value'),
            ('PowerSupply_price', 'PowerSupply price'),
        )),
        ('Other', (
            ('Other_budget', 'Budget'),
            ('Other_os', 'OS'),
        )),
    ]

    title = models.CharField(max_length=256)
    next = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, blank=True)
    component = models.CharField(max_length=20, choices=MEDIA_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.title


class Build(models.Model):
    title = models.CharField(max_length=256)
    cpu = models.ForeignKey(CPU, on_delete=models.SET_NULL, null=True)
    gpu = models.ForeignKey(GPU, on_delete=models.SET_NULL, null=True)
    motherboard = models.ForeignKey(MotherBoard, on_delete=models.SET_NULL, null=True)
    ram = models.ManyToManyField(RAM)
    rom = models.ManyToManyField(ROM)
    powersupply = models.ForeignKey(PowerSupply, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
