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
    model = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    cores = models.IntegerField()
    threads = models.IntegerField()
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    benchmark = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class GPU(models.Model):
    model = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    memory = models.IntegerField()
    benchmark = models.IntegerField()
    price = models.IntegerField()
    power = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class RAM(models.Model):
    model = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.IntegerField()
    benchmark = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class MotherBoard(models.Model):
    model = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    chipset = models.ForeignKey(Chipset, on_delete=models.CASCADE)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE)
    value = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class ROM(models.Model):
    TYPE = (
        ('H', 'HDD'),
        ('S', 'SSD'),
    )

    model = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE, default='H')
    read = models.IntegerField()
    write = models.IntegerField()
    size = models.IntegerField()
    benchmark = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model


class PowerSupply(models.Model):
    model = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    power = models.IntegerField()
    value = models.IntegerField()
    price = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return self.model
