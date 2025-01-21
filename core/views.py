from django.shortcuts import render
from .models import Goal, Meditation
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
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


@login_required
def edit_goal(request, id):
    goal = Goal.objects.get(id=id)
    if request.method == 'POST':
        goal.title = request.POST['title']
        goal.status = request.POST['status']
        goal.save()
        return HttpResponseRedirect('/')
    return render(request, 'edit_goal.html', {'goal': goal})


@login_required
def add_goal(request):
    context = request.GET.get('context', 'private')
    goal_type = request.GET.get('goal_type', 'weekly')
    if request.method == 'POST':
        title = request.POST['title']
        status = request.POST['status']
        highest_priority_goal = Goal.objects.filter(
            context=context,
            goal_type=goal_type).order_by('-priority').first()
        highest_priority = (highest_priority_goal.priority
                            if highest_priority_goal else 0)
        Goal.objects.create(title=title, status=status, context=context,
                            goal_type=goal_type, priority=highest_priority + 1)
        return HttpResponseRedirect('/')
    return render(request, 'add_goal.html', {'context': context,
                                             'goal_type': goal_type})


@login_required
def delete_goal(request, id):
    goal = Goal.objects.get(id=id)
    if request.method == 'POST':
        goal.delete()
        return HttpResponseRedirect('/')
    return render(request, 'edit_goal.html', {'goal': goal})


@login_required
def all_goals(request):
    context = request.GET.get('context', 'private')
    if request.method == 'POST':
        for goal_id, title in request.POST.items():
            if goal_id.startswith('title_'):
                goal = Goal.objects.get(id=goal_id.split('_')[1])
                goal.title = title
                goal.save()
        for goal_id, priority in request.POST.items():
            if goal_id.startswith('priority_'):
                goal = Goal.objects.get(id=goal_id.split('_')[1])
                goal.priority = priority
                goal.save()
        return HttpResponseRedirect('/goals/?context=' + context)

    quarterly_goals = Goal.objects.filter(
        context=context,
        goal_type='quarterly').order_by('priority')
    weekly_goals = Goal.objects.filter(
        context=context,
        goal_type='weekly').order_by('priority')
    return render(request, 'all_goals.html',
                  {'quarterly_goals': quarterly_goals,
                   'weekly_goals': weekly_goals,
                   'context': context})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html',
                          {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')
