from pcbcore.models import *


class ComponentVariable(models.Model):
    title = models.CharField(max_length=32)
    MEDIA_CHOICES_TYPE = [
        ('int', 'int'),
        ('float', 'float'),
        ('string', 'string'),
        ('bool', 'bool')
    ]
    MEDIA_CHOICES_COMPONENT = [
        ('CPU', (
            ('CPU_model', 'CPU model'),
            ('CPU_brand', 'CPU brand'),
            ('CPU_cores', 'CPU cores'),
            ('CPU_threads', 'CPU threads'),
            ('CPU_frequency', 'CPU frequency'),
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
        ('MB', (
            ('MotherBoard_model', 'MotherBoard model'),
            ('MotherBoard_brand', 'MotherBoard brand'),
            ('MotherBoard_formfactor', 'MotherBoard formfactor'),
            ('MotherBoard_chipset', 'MotherBoard chipset'),
            ('MotherBoard_socket', 'MotherBoard socket'),
            ('MotherBoard_year', 'MotherBoard year'),
            ('MotherBoard_price', 'MotherBoard price'),
        )),
        ('SSD', (
            ('SSD_model', 'SSD model'),
            ('SSD_brand', 'SSD brand'),
            ('SSD_benchmark', 'SSD benchmark'),
            ('SSD_formfactor', 'SSD formfactor'),
            ('SSD_capacity', 'SSD capacity'),
            ('SSD_price', 'SSD price'),
        )),
        ('HDD', (
            ('HDD_model', 'HDD model'),
            ('HDD_brand', 'HDD brand'),
            ('HDD_benchmark', 'HDD benchmark'),
            ('HDD_formfactor', 'HDD formfactor'),
            ('HDD_capacity', 'HDD capacity'),
            ('HDD_price', 'HDD price'),
        )),
        ('PS', (
            ('PowerSupply_model', 'PowerSupply model'),
            ('PowerSupply_brand', 'PowerSupply brand'),
            ('PowerSupply_power', 'PowerSupply power'),
            ('PowerSupply_value', 'PowerSupply value'),
            ('PowerSupply_price', 'PowerSupply price'),
        )),
        ('Other', (
            ('Other_budget', 'Budget'),
            ('Other_os', 'OS'),
        ))
    ]
    type = models.CharField(max_length=6, choices=MEDIA_CHOICES_TYPE)
    component = models.CharField(max_length=32, choices=MEDIA_CHOICES_COMPONENT)

    def __str__(self):
        return self.title


class Factor(models.Model):
    MEDIA_CHOICES_COMPONENT = [
        ('CPU', 'CPU'),
        ('GPU', 'GPU'),
        ('RAM', 'RAM'),
        ('MB', 'MotherBoard'),
        ('SSD', 'SSD'),
        ('HDD', 'HDD'),
        ('PS', 'PowerSupply'),
    ]

    component = models.CharField(max_length=3, choices=MEDIA_CHOICES_COMPONENT, null=True, blank=True)
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
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    next = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, blank=True)
    component_variable = models.ForeignKey(ComponentVariable, on_delete=models.SET_NULL, null=True, blank=True)
    is_first = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.title


class Build(models.Model):
    title = models.CharField(max_length=256)
    cpu = models.ForeignKey(CPU, on_delete=models.SET_NULL, null=True)
    gpu = models.ForeignKey(GPU, on_delete=models.SET_NULL, null=True)
    motherboard = models.ForeignKey(MotherBoard, on_delete=models.SET_NULL, null=True)
    ram = models.ForeignKey(RAM, on_delete=models.SET_NULL, null=True)
    ssd = models.ForeignKey(SSD, on_delete=models.SET_NULL, null=True)
    hdd = models.ForeignKey(HDD, on_delete=models.SET_NULL, null=True)
    powersupply = models.ForeignKey(PowerSupply, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(default=0)
    benchmark = models.FloatField(default=0)
    os = models.BooleanField(default=False)
    factors = {
        'CPU': 0,
        'GPU': 0,
        'RAM': 0,
        'MB': 0,
        'SSD': 0,
        'HDD': 0,
        'PS': 0
    }
    part = []

    def recalculate_price(self):
        self.price = 0
        for item in self.part:
            self.price += item.get_price()

    def recalculate_benchmark(self):
        self.benchmark = 0
        for item in self.part:
            self.benchmark += item.get_benchmark()
        self.benchmark = round(self.benchmark, 1)

    def recalculate_part(self):
        self.part.clear()
        if self.cpu is not None:
            self.part.append(self.cpu)
        if self.gpu is not None:
            self.part.append(self.gpu)
        if self.motherboard is not None:
            self.part.append(self.motherboard)
        if self.powersupply is not None:
            self.part.append(self.powersupply)
        if self.ram is not None:
            self.part.append(self.ram)
        if self.ssd is not None:
            self.part.append(self.ssd)
        if self.hdd is not None:
            self.part.append(self.hdd)

    def build(self, budget, func):
        normalize(self.factors)

        self.factors = {key: val for key, val in self.factors.items() if val != 0.0}

        while len(self.factors) > 0:
            minimal_factor = func(self.factors, key=self.factors.get)
            if minimal_factor == 'CPU':
                self.cpu = get_by_budget_or_minimal(CPU, budget * self.factors['CPU'], '-benchmark')
                budget -= self.cpu.price
            if minimal_factor == 'GPU':
                self.gpu = get_by_budget_or_minimal(GPU, budget * self.factors['GPU'], '-benchmark')
                budget -= self.gpu.price
            if minimal_factor == 'RAM':
                self.ram = get_by_budget_or_minimal(RAM, budget * self.factors['RAM'], '-benchmark')
                budget -= self.ram.price
            if minimal_factor == 'SSD':
                self.ssd = get_by_budget_or_minimal(SSD, budget * self.factors['SSD'], '-benchmark')
                budget -= self.ssd.price
            if minimal_factor == 'HDD':
                self.hdd = get_by_budget_or_minimal(HDD, budget * self.factors['HDD'], '-benchmark')
                budget -= self.hdd.price
            if minimal_factor == 'MB':
                self.motherboard = get_by_budget_or_minimal(MotherBoard, budget * self.factors['MB'], '-year')
                budget -= self.motherboard.price
            if minimal_factor == 'PS':
                self.powersupply = get_by_budget_or_minimal(PowerSupply, budget * self.factors['PS'], '-power')
                budget -= self.powersupply.price
            self.factors.pop(minimal_factor)
            normalize(self.factors)

        self.recalculate_part()
        self.recalculate_price()
        self.recalculate_benchmark()


def normalize(d):
    if sum(d.values()) == 0:
        return
    factor = 1.0 / sum(d.values())
    for k in d:
        d[k] = d[k] * factor
