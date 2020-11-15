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


class CPU(models.Model):
    model = models.CharField(max_length=128, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    cores = models.IntegerField()
    threads = models.IntegerField()
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    benchmark = models.FloatField()
    frequency = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return f'{self.brand} {self.model}'

    def get_url(self):
        return format_html(f'<a href="{self.url}">{self.url}</a>')

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPUs'


class GPU(models.Model):
    model = models.CharField(max_length=128, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    memory = models.IntegerField()
    benchmark = models.FloatField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return f'{self.brand} {self.model}'

    def get_url(self):
        return format_html(f'<a href="{self.url}">{self.url}</a>')

    class Meta:
        verbose_name = 'GPU'
        verbose_name_plural = 'GPUs'


class MemoryType(models.Model):
    title = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.title


class RAM(models.Model):
    model = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.ForeignKey(MemoryType, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    capacity = models.IntegerField()
    count = models.IntegerField()
    benchmark = models.FloatField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return f'{self.brand} {self.model}'

    def get_url(self):
        return format_html(f'<a href="{self.url}">{self.url}</a>')

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


class MotherBoard(models.Model):
    model = models.CharField(max_length=128, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    formfactor = models.ForeignKey(Formfactor, on_delete=models.CASCADE)
    chipset = models.ForeignKey(Chipset, on_delete=models.CASCADE)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return f'{self.brand} {self.model}'

    def get_url(self):
        return format_html(f'<a href="{self.url}">{self.url}</a>')


class SSD(models.Model):
    model = models.CharField(max_length=128, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    benchmark = models.FloatField()
    price = models.IntegerField()
    formfactor = models.ForeignKey(Formfactor, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return f'{self.brand} {self.model}'

    def get_url(self):
        return format_html(f'<a href="{self.url}">{self.url}</a>')

    class Meta:
        verbose_name = 'SSD'
        verbose_name_plural = 'SSDs'


class HDD(models.Model):
    model = models.CharField(max_length=128, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    benchmark = models.FloatField()
    price = models.IntegerField()
    formfactor = models.ForeignKey(Formfactor, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return f'{self.brand} {self.model}'

    def get_url(self):
        return format_html(f'<a href="{self.url}">{self.url}</a>')

    class Meta:
        verbose_name = 'HDD'
        verbose_name_plural = 'HDDs'


class PowerSupply(models.Model):
    model = models.CharField(max_length=128, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    power = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f'{self.brand} {self.model}'
