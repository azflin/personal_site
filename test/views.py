from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from time import sleep

data = {}

# Create your views here.
def index(request):
    return render(request, 'test/index.html')


def test_function(request):
    data['foo'] = 0
    while data['foo'] < 10:
        print data['foo']
        data['foo'] += 1
        sleep(1)
    return JsonResponse({'output': 'swagz'})


def test_poll(request):
    curr = data['foo']
    while data['foo'] == curr:
        print "Data didnt change yet bruh"
        pass
    if data['foo'] == 10:
        return JsonResponse({'done': True})
    else:
        return JsonResponse({'data': data['foo'], 'done': False})