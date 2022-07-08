from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout


def home(request):
    return render(request, 'todoapp/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todoapp/signupuser.html', {'form': UserCreationForm(),
                                                                   'error': 'The user name already exist. Please choose a new username'})

        else:
            return render(request, 'todoapp/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Password didnt match'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currenttodos(request):
    return render(request, 'todoapp/currenttodos.html')
