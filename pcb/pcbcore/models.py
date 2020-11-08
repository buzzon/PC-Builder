from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


class Socket(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


class CPU(models.Model):
    model = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    cores = models.IntegerField()
    threads = models.IntegerField()
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    benchmark = models.FloatField()
    frequency = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class GPU(models.Model):
    model = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    memory = models.IntegerField()
    benchmark = models.FloatField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class MemoryType(models.Model):
    title = models.CharField(max_length=16)

    def __str__(self):
        return self.title


class RAM(models.Model):
    model = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.ForeignKey(MemoryType, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    capacity = models.CharField(max_length=16)
    benchmark = models.FloatField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class Formfactor(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Chipset(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


class MotherBoard(models.Model):
    model = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    formfactor = models.ForeignKey(Formfactor, on_delete=models.CASCADE)
    chipset = models.ForeignKey(Chipset, on_delete=models.CASCADE)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class ROM(models.Model):
    TYPE = (
        ('H', 'HDD'),
        ('S', 'SSD'),
    )

    model = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE, default='H')
    read = models.IntegerField()
    write = models.IntegerField()
    size = models.IntegerField()
    benchmark = models.FloatField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class PowerSupply(models.Model):
    model = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    power = models.IntegerField()
    value = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model
