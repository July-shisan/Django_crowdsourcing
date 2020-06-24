import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .form import registerForm, loginForm, challengeForm
# Create your views here.
from demo.models import User, Challenge, Developer
from django.views.generic import View
from django.db import connection
from ML_Models.recommend import recommend
from ML_Models.developerRec import developerRec
from django.http import HttpResponseRedirect


# def home(request):
#     return render(request, 'home.html')
def get_corsor():
    return connection.cursor()

class homeView(View):
    def get(self, request):
        challenge = Challenge.objects.all().order_by('-release_time')
        data = {
            "title": "BUAA",
            "challenge": challenge,
        }
        return render(request, 'home.html', context=data)

# def release(request):
#     return render(request, 'release.html')
class releaseView(View):
    def get(self, request):
        return render(request, 'release.html')
    def post(self, request):
        form = challengeForm(request.POST or None)
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        if form.is_valid():
            chal = form.save(commit=False)
            # chal.chtype = request.POST.get('chtype')
            chal.hoster = user
            chal.save()
            request.session['chId'] = chal.chId
            return redirect(reverse('details'))
        else:
            print(form.errors.get_json_data())
            return redirect(reverse('release'))

def alldeveloper(request):
    return render(request, 'developers.html')
def details(request):
    ch_id = request.session.get('chId')
    challenge = Challenge.objects.get(pk=ch_id)
    # recdevelopers = recommend(challenge)
    recdevelopers = developerRec(challenge)
    names = []
    i = 0
    for d in recdevelopers:
        i += 1
        if i >= 5:
            break
        developer = Developer.objects.get(devename=d)
        names.append(developer)
    data = {
        "title": "Details",
        "challenge": challenge,
        "name": names,
    }
    return render(request, 'details.html', context=data)
def task(request, taskId):
    id = int(taskId)
    task = Challenge.objects.get(chId=id)
    data = {
        "title": "TaskDetails",
        "task": task,
        "hoster": task.hoster
    }
    return render(request, 'task.html', context=data)

def developer(request, deveId):
    id = int(deveId)
    deve = Developer.objects.get(deveId=id)
    data = {
        "deve": deve,
    }
    return render(request, 'developerDetail.html', context=data)
# def register(request):
#     if request.method == 'GET':
#         data = {
#             'title': "register"
#         }
#         return render(request, 'register.html')
#     elif request.method == 'POST':
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         email = request.POST.get("email")
#         register_time = datetime.datetime.now().strftime('%Y-%m-%d')
#         user = User()
#         user.username =username
#         user.password = password
#         user.email = email
#         user.register_time = register_time
#         user.save()
#         return render(request, 'register.html')
# def login(request):
#     return render(request, 'login.html')
def logout(request):
    request.session.flush()
    return redirect(reverse('home'))
def profile(request, userId):
    id = int(userId)
    user = User.objects.get(pk=id)
    hist_chal = user.challenge_set.all()
    data = {
        "title": "profile",
        "user": user,
        "history": hist_chal
    }
    return render(request, 'profile.html', context=data)

class loginView(View):
    def get(self, request):
        data = {
            "title": "login"
        }
        return render(request, 'login.html',context=data)
    def post(self, request):
        form = loginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username, password=password).first()
            if user:
                request.session['user_id'] = user.userId
                response = redirect(reverse('home'))
                response.set_cookie("username", username)
                response.set_cookie("password", password)
                return response
            else:
                print('用户名或密码错误')
                return redirect(reverse('login'))
        else:
            print(form.errors.get_json_data())
            return redirect(reverse('login'))

class registerView(View):
    def get(self, request):
        data = {
            "title": "register"
        }
        return render(request, 'register.html', context=data)
    def post(self, request):
        form = registerForm(request.POST or None)
        # form.register_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        else:
            errors = form.errors
            print(errors)
            return redirect(reverse('register'))
