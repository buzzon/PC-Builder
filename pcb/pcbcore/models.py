from django.db import models
from django.utils.html import format_html


class Brand(models.Model):
    objects = None
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


class Socket(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


def get_by_budget_or_minimal(self, budget, order):
    if budget == 0.0:
        return None
    part = next(iter(self.objects.filter(price__lte=budget).order_by(order)), None)
    if part is None:
        part = next(iter(self.objects.order_by('price')), None)
    return part


class Part(models.Model):
    model = models.CharField(max_length=128, default="None")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default="None")
    benchmark = models.FloatField()
    price = models.IntegerField()
    url = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.brand} {self.model}'

    def get_url(self):
        return format_html(f'<a href="{self.url}">{self.url}</a>')


class CPU(Part):
    cores = models.IntegerField()
    threads = models.IntegerField()
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    frequency = models.IntegerField()

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPUs'


class GPU(Part):
    memory = models.IntegerField()

    class Meta:
        verbose_name = 'GPU'
        verbose_name_plural = 'GPUs'


class MemoryType(models.Model):
    title = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.title


class RAM(Part):
    type = models.ForeignKey(MemoryType, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    capacity = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = 'RAMs'


class Formfactor(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


class Chipset(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


class MotherBoard(Part):
    formfactor = models.ForeignKey(Formfactor, on_delete=models.CASCADE)
    chipset = models.ForeignKey(Chipset, on_delete=models.CASCADE)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    year = models.IntegerField()
    benchmark = None


class SSD(Part):
    formfactor = models.ForeignKey(Formfactor, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    class Meta:
        verbose_name = 'SSD'
        verbose_name_plural = 'SSDs'


class HDD(Part):
    formfactor = models.ForeignKey(Formfactor, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    class Meta:
        verbose_name = 'HDD'
        verbose_name_plural = 'HDDs'


class PowerSupply(Part):
    power = models.IntegerField()
    benchmark = None
    url = None
