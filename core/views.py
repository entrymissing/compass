from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Goal, Meditation
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect


@login_required
def index(request):
    context = request.GET.get('context', 'private')
    goals = Goal.objects.filter(context=context).values().order_by('priority')
    goals_list = list(goals)
    meditations = list(Meditation.objects.values())
    meditation = random.choice(meditations) if meditations else None
    return render(request, 'index.html', {'goals': goals_list,
                                          'context': context,
                                          'meditation': meditation})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')
