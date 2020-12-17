from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime

from pcbcore.models import *
from pcbknowledge.models import Question, Essence, Build


def index(request):
    cpu_count = CPU.objects.count()
    gpu_count = GPU.objects.count()
    ram_count = RAM.objects.count()
    mother_board_count = MotherBoard.objects.count()
    ssd_count = SSD.objects.count()
    hdd_count = HDD.objects.count()
    power_supply_count = PowerSupply.objects.count()
    first_question_id = Question.objects.filter(is_first=True)[0].id
    builds = Build.objects.all().order_by('-title')

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
            'first_question_id': first_question_id,
            'builds': builds
        }
    )


def questions(request):
    build = Build()
    build_other = Build()
    difference = {}

    template = 'question.html'
    history = {}
    question = "The knowledge base is not yet full :c"
    budget = 0

    if Question.objects.count() > 0:
        if 'start' in request.POST:
            question_id = request.POST.get("question_id_next", -1)
            question = get_object_or_404(Question, pk=question_id)
            request.session['history'] = {}
        if 'next' in request.POST:
            history = request.session.get('history', {})
            question_id = request.POST.get("question_id_next", -1)
            question = get_object_or_404(Question, pk=question_id)
            old_question_id = request.POST.get("question_id", -1)
            old_question = get_object_or_404(Question, pk=old_question_id)

            component = request.POST.get("component_data", None)
            component_is_id = request.POST.get("component_is_id", False)
            factors_format = request.POST.get("component", '')
            if component is not None and component_is_id:
                factors_format = {}
                essence = Essence.objects.filter(pk=component)[0]
                build.factors = list(essence.factors.all())
                component = essence.title

                for factor in build.factors:
                    factors_format[factor.component] = factor.coefficient

            history[old_question.title] = [component, factors_format]
            request.session['history'] = history
        elif 'build' in request.POST:
            template = 'build.html'
            history = request.session.get('history', {})
            old_question_id = request.POST.get("question_id", -1)
            old_question = get_object_or_404(Question, pk=old_question_id)

            component = request.POST.get("component_data", None)
            component_is_id = request.POST.get("component_is_id", False)
            factors_format = request.POST.get("component", '')
            if component is not None and component_is_id:
                factors_format = {}
                essence = Essence.objects.filter(pk=component)[0]
                build.factors = list(essence.factors.all())
                component = essence.title

                for factor in build.factors:
                    factors_format[factor.component] = factor.coefficient

            history[old_question.title] = [component, factors_format]
            request.session['history'] = history

            for item in history.items():
                if isinstance(item[1][1], dict):
                    for factor_item in item[1][1].items():
                        build.factors[factor_item[0]] = build.factors[factor_item[0]] + factor_item[1]
                else:
                    if item[1][1] == 'Other_budget':
                        budget = item[1][0]
                    elif item[1][1] == 'Other_os':
                        build.os = bool(item[1][0])

            build.title = datetime.now()
            build_other.title = datetime.now()
            build_other.factors = build.factors
            build.build(int(budget), min)
            build_other.build(int(budget) + int(budget)*0.1, max)
            difference['price'] = build_other.price - build.price
            difference['benchmark'] = round(build_other.benchmark - build.benchmark, 1)

            build.save()
            build_other.save()

    return render(
        request,
        template,
        context={
            'question': question,
            'history': history,
            'build': build,
            'build_other': build_other,
            'difference': difference,
        }
    )
