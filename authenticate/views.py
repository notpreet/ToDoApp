from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from django.contrib.auth import logout, login
from django.contrib.auth.models import User, auth
from .models import UserData, Tasks



# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST.get('pwd')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def home(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        if request.method == 'GET' and 'task_status' in request.GET:
            task_stat = request.GET['task_status']
            if task_stat == 'AC':
                request.session['task_status'] = 'AC'
            elif task_stat == 'CO':
                request.session['task_status'] = 'CO'
            else:
                request.session['task_status'] = ''
        if Tasks.objects.filter(username__pk=user_id):
            tasks = Tasks.objects.filter(username=UserData.objects.get(pk=user_id))
        else:
            tasks = None
        if tasks is not None:
            return render(request, 'home.html', {'task': tasks})
        else:
            return render(request, 'home.html', {'task': None})
    else:
        return redirect('index')


def register(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        profilepic = request.FILES['profilepic']
        if pass1 == pass2:
            user = User.objects.create_user(username=username, password=pass1, email=email)
            userdata = UserData(username=username, firstname=firstname, lastname=lastname, email=email, profilepic=profilepic)
            user.save()
            userdata.save()
            return render(request, 'index.html')
        else:
            print('password not same')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')


def createteask(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        username = request.user.id
        task = Tasks(username=UserData.objects.get(pk=username), task_name=task_name)
        task.save()
        return redirect('home')
    else:
        return render(request, 'createTask.html')


