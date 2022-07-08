from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo


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


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoapp/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password didnt match'})
        else:
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todoapp/currenttodos.html', {'todos': todos})


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todoapp/createtodo.html', {'form': TodoForm()})

    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoapp/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again'})
