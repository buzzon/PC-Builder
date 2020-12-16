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
    cpu = None
    gpu = None
    ram = None
    mb = None
    ssd = None
    hdd = None
    ps = None

    template = 'question.html'
    history = {}
    question = "The knowledge base is not yet full :c"
    budget = 0
    need_os = False
    price = 0
    factors = {
        'CPU': 0,
        'GPU': 0,
        'RAM': 0,
        'MB': 0,
        'SSD': 0,
        'HDD': 0,
        'PS': 0
    }

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
                factors = list(essence.factors.all())
                component = essence.title

                for factor in factors:
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
                factors = list(essence.factors.all())
                component = essence.title

                for factor in factors:
                    factors_format[factor.component] = factor.coefficient

            history[old_question.title] = [component, factors_format]
            request.session['history'] = history

            for item in history.items():
                if isinstance(item[1][1], dict):
                    for factor_item in item[1][1].items():
                        factors[factor_item[0]] = factors[factor_item[0]] + factor_item[1]
                else:
                    if item[1][1] == 'Other_budget':
                        budget = item[1][0]
                    elif item[1][1] == 'Other_os':
                        need_os = item[1][0]

            normalize(factors)

            cpu = get_by_budget_or_minimal(CPU, int(budget) * factors['CPU'], '-benchmark')
            gpu = get_by_budget_or_minimal(GPU, int(budget) * factors['GPU'], '-benchmark')
            ram = get_by_budget_or_minimal(RAM, int(budget) * factors['RAM'], '-benchmark')
            mb = get_by_budget_or_minimal(MotherBoard, int(budget) * factors['MB'], '-year')
            ssd = get_by_budget_or_minimal(SSD, int(budget) * factors['SSD'], '-benchmark')
            hdd = get_by_budget_or_minimal(HDD, int(budget) * factors['HDD'], '-benchmark')
            ps = get_by_budget_or_minimal(PowerSupply, int(budget) * factors['PS'], '-power')

            if cpu is not None:
                price += cpu.price
            if gpu is not None:
                price += gpu.price
            if ram is not None:
                price += ram.price
            if mb is not None:
                price += mb.price
            if ssd is not None:
                price += ssd.price
            if hdd is not None:
                price += hdd.price
            if ps is not None:
                price += ps.price

    return render(
        request,
        template,
        context={
            'question': question,
            'history': history,
            'factors': factors,
            'cpu': cpu,
            'gpu': gpu,
            'ram': ram,
            'mb': mb,
            'ssd': ssd,
            'hdd': hdd,
            'ps': ps,
            'price': price
        }
    )


def normalize(d):
    dd = d.values()
    ddd = sum(d.values())
    factor = 1.0/sum(d.values())
    for k in d:
        d[k] = d[k] * factor
