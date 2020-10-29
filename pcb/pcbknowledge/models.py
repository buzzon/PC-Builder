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

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=256)
    next = models.OneToOneField('Question', on_delete=models.SET_NULL, null=True, blank=True)
    build = models.OneToOneField('Build', on_delete=models.SET_NULL, null=True, blank=True)

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
