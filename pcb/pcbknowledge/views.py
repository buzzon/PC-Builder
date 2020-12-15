from django.shortcuts import render, get_object_or_404

from pcbcore.models import *
from pcbknowledge.models import Question, Factor, Essence


def index(request):
    cpu_count = CPU.objects.count()
    gpu_count = GPU.objects.count()
    ram_count = RAM.objects.count()
    mother_board_count = MotherBoard.objects.count()
    ssd_count = SSD.objects.count()
    hdd_count = HDD.objects.count()
    power_supply_count = PowerSupply.objects.count()
    first_question_id = Question.objects.filter(is_first=True)[0].id

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
            'first_question_id': first_question_id
        }
    )


def questions(request):
    template = 'question.html'
    history = {}
    question = "The knowledge base is not yet full :c"

    if Question.objects.count() > 0:
        if 'start' in request.POST:
            question_id = request.POST.get("question_id_next", -1)
            question = get_object_or_404(Question, pk=question_id)
            request.session['history'] = {}
        if 'next' in request.POST:
            history = request.session.get('history', {})
            question_id = request.POST.get("question_id_next", -1)
            question = get_object_or_404(Question, pk=question_id)

            component = request.POST.get("component", '')
            component_data = request.POST.get("component_data", None)
            factors_format = {}
            if component_data is not None:
                essence = Essence.objects.filter(pk=component_data)[0]
                factors = list(essence.factors.all())

                for factor in factors:
                    factors_format[factor.component] = factor.coefficient

            old_question_id = request.POST.get("question_id", -1)
            old_question = get_object_or_404(Question, pk=old_question_id)

            history[old_question.title] = [component, factors_format]
            request.session['history'] = history
        elif 'build' in request.POST:
            history = request.session.get('history', {})

            component = request.POST.get("component", '')
            component_data = request.POST.get("component_data", '')
            old_question_id = request.POST.get("question_id", -1)
            old_question = get_object_or_404(Question, pk=old_question_id)

            history[old_question.title] = [component, component_data]
            request.session['history'] = history
            template = 'build.html'
    return render(
        request,
        template,
        context={
            'question': question,
            'history': history
        }
    )