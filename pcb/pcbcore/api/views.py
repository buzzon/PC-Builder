from django.http import HttpResponse


def index(request):
    test = int(request.GET['test'])
    return HttpResponse(test*2)

