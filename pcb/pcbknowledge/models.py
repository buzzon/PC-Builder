from pcbcore.models import *


class Component(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Factor(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    coefficient = models.IntegerField()
    essence = models.ForeignKey('Essence', related_name='factors', on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.coefficient}] {self.component}'


class Essence(models.Model):
    title = models.CharField(max_length=256)
    question = models.ForeignKey('Question', related_name='essences', on_delete=models.CASCADE)
    next_question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='next_question')

    def __str__(self):
        return self.title


class Question(models.Model):
    MEDIA_CHOICES = [
        ('CPU', (
            ('CPU_model', 'CPU model'),
            ('CPU_brand', 'CPU brand'),
            ('CPU_cores', 'CPU cores'),
            ('CPU_threads', 'CPU threads'),
            ('CPU_socket', 'CPU socket'),
            ('CPU_benchmark', 'CPU benchmark'),
            ('CPU_frequency', 'CPU frequency'),
            ('CPU_price', 'CPU price'),
        )),
        ('GPU', (
            ('GPU_model', 'GPU model'),
            ('GPU_brand', 'GPU brand'),
            ('GPU_memory', 'GPU memory'),
            ('GPU_benchmark', 'GPU benchmark'),
            ('GPU_price', 'GPU price'),
        )),
        ('MotherBoard', (
            ('MotherBoard_model', 'MotherBoard model'),
            ('MotherBoard_brand', 'MotherBoard brand'),
            ('MotherBoard_formfactor', 'MotherBoard formfactor'),
            ('MotherBoard_chipset', 'MotherBoard chipset'),
            ('MotherBoard_socket', 'MotherBoard socket'),
            ('MotherBoard_year', 'MotherBoard year'),
            ('MotherBoard_price', 'MotherBoard price'),
        )),
        ('RAM', (
            ('RAM_model', 'RAM model'),
            ('RAM_brand', 'RAM brand'),
            ('RAM_type', 'RAM type'),
            ('RAM_frequency', 'RAM frequency'),
            ('RAM_capacity', 'RAM capacity'),
            ('RAM_count', 'RAM count'),
            ('RAM_benchmark', 'RAM benchmark'),
            ('RAM_price', 'RAM price'),
        )),
        ('HDD', (
            ('HDD_model', 'HDD model'),
            ('HDD_brand', 'HDD brand'),
            ('HDD_benchmark', 'HDD benchmark'),
            ('HDD_formfactor', 'HDD formfactor'),
            ('HDD_capacity', 'HDD capacity'),
            ('HDD_price', 'HDD price'),
        )),
        ('SSD', (
            ('SSD_model', 'SSD model'),
            ('SSD_brand', 'SSD brand'),
            ('SSD_benchmark', 'SSD benchmark'),
            ('SSD_formfactor', 'SSD formfactor'),
            ('SSD_capacity', 'SSD capacity'),
            ('SSD_price', 'SSD price'),
        )),
        ('PowerSupply', (
            ('PowerSupply_model', 'PowerSupply model'),
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

    title = models.TextField()
    next = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, blank=True)
    component = models.CharField(max_length=32, choices=MEDIA_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.title


class Build(models.Model):
    title = models.CharField(max_length=256)
    cpu = models.ForeignKey(CPU, on_delete=models.SET_NULL, null=True)
    gpu = models.ForeignKey(GPU, on_delete=models.SET_NULL, null=True)
    motherboard = models.ForeignKey(MotherBoard, on_delete=models.SET_NULL, null=True)
    ram = models.ManyToManyField(RAM)
    ssd = models.ManyToManyField(SSD)
    hdd = models.ManyToManyField(HDD)
    powersupply = models.ForeignKey(PowerSupply, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
