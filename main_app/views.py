from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('<h1>Home Page</h1>')

def team_detail(request):
    return HttpResponse('<h1>Team Detail</h1>')


def game_detail(request):
    return HttpResponse('<h1>Game Detail</h1>')