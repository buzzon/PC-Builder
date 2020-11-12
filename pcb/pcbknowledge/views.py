from django.db.models import Min
from django.shortcuts import render

from pcbcore.models import *
from pcbknowledge.models import Question


def index(request):
    cpu_count = CPU.objects.count()
    gpu_count = GPU.objects.count()
    ram_count = RAM.objects.count()
    mother_board_count = MotherBoard.objects.count()
    ssd_count = SSD.objects.count()
    hdd_count = HDD.objects.count()
    power_supply_count = PowerSupply.objects.count()

    return render(
        request,
        'index.html',
        context={
            'cpu_count': cpu_count,
            'gpu_count': gpu_count,
            'ram_count': ram_count,
            'mother_board_count': mother_board_count,
            'ssd_count': ssd_count,
            'hdd_count': hdd_count,
            'power_supply_count': power_supply_count,
        }
    )


def questions(request):
    if Question.objects.count() > 0:
        question = Question.objects.filter().values_list('title')
        # question = Question.objects.filter().values_list('title').annotate(Min('id')).order_by('id')[0][0]
    else:
        question = "База знаний ещё не заполнена :с"
    return render(
        request,
        'question.html',
        context={
            'question': question
        }
    )
