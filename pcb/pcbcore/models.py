from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.title


class Socket(models.Model):
    title = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.title


class Chipset(models.Model):
    title = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.title


class CPU(models.Model):
    title = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    cores = models.IntegerField()
    threads = models.IntegerField()
    frequency = models.FloatField()
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    value = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.title


class GPU(models.Model):
    title = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    memory = models.IntegerField()
    value = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.title


class RAM(models.Model):
    title = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    frequency = models.FloatField()
    size = models.IntegerField()
    value = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.title


class MotherBoard(models.Model):
    title = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    chipset = models.ForeignKey(Chipset, on_delete=models.CASCADE)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    value = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.title


class ROM(models.Model):
    TYPE = (
        ('H', 'HDD'),
        ('S', 'SSD'),
    )

    title = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE, default='H')
    read = models.IntegerField()
    write = models.IntegerField()
    size = models.IntegerField()
    value = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.title


class PowerSupply(models.Model):
    title = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    power = models.IntegerField()
    value = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.title
