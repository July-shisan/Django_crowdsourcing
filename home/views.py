import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .form import registerForm, loginForm, challengeForm, develoginForm, uploadForm, deveregisterForm
# Create your views here.
from home.models import User, Challenge, Developer, SolutionFile
from django.views.generic import View
from django.db import connection
from ML_Models.recommend import recommend
from ML_Models.developerRec import developerRec
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from CrowdPlat.settings import MEDIA_ROOT
from .PreTec.eval import pre_technology
import pandas as pd
import os
from sklearn.metrics import roc_auc_score

# def home(request):
#     return render(request, 'home.html')
def get_corsor():
    return connection.cursor()

class homeView(View):
    def get(self, request):
        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 5))
        challenge = Challenge.objects.all().order_by('-release_time')
        paginator = Paginator(challenge , per_page)
        page_object = paginator.page(page)
        data = {
            "page_object": page_object,
            "page_range": paginator.page_range,
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
            messages.success(request, "请填写完整信息！")
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
        try:
            developer = Developer.objects.get(devename=d)
        except:
            data = {
                "title": "Details",
                "challenge": challenge,
                "name": names,
            }
            return render(request, 'details.html', context=data)
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
    devel = Developer.objects.get(deveId=request.session.get('deve_id'))
    data = {
        "title": "TaskDetails",
        "task": task,
        "hoster": task.hoster,
        "devel": devel
    }
    if devel.challenge_set.all().filter(chId=id):
        return render(request, 'intask.html', context=data)
    else:
        return render(request, 'task.html', context=data)
def intask(request, taskId):
    id = int(taskId)
    task = Challenge.objects.get(chId=id)
    devel = Developer.objects.get(deveId=request.session.get('deve_id'))
    task.user_task.add(devel)
    data = {
        "title": "TaskDetails",
        "task": task,
        "hoster": task.hoster,
        "devel": devel
    }
    messages.success(request, "已加入任务！")
    return render(request, 'intask.html', context=data)

def developer(request, deveId):
    id = int(deveId)
    deve = Developer.objects.get(deveId=id)
    data = {
        "deve": deve,
    }
    return render(request, 'developerDetail.html', context=data)

def logout(request):
    request.session.flush()
    response = redirect(reverse('home'))
    response.delete_cookie('userId')
    response.delete_cookie('username')
    response.delete_cookie('password')
    messages.success(request, "已退出登录！")
    return response
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
        return render(request, 'login.html', context=data)
    def post(self, request):
        next = request.GET.get('next', '')
        if next == '/login/' or next == '/register/' or len(next) == 0:
            next = '/'
        form = loginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username, password=password).first()
            if user:
                request.session['user_id'] = user.userId
                # response = redirect(reverse('home'))
                response = HttpResponseRedirect(next)
                response.set_cookie("userId", user.userId)
                response.set_cookie("username", username)
                response.set_cookie("password", password)
                return response
            else:
                print('用户名或密码错误')
                messages.success(request, "用户名或密码错误!")
                return redirect(reverse('login'))
        else:
            print(form.errors.get_json_data())
            messages.success(request, "用户名或密码错误!")
            return redirect(reverse('login'))
class develogin(View):
    def get(self, request):
        data = {
            "title": "develogin"
        }
        return render(request, 'develogin.html', context=data)
    def post(self, request):
        next = request.GET.get('next', '')
        if next == '/login/' or next == '/register/' or len(next) == 0:
            next = '/'
        form = develoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('devename')
            password = form.cleaned_data.get('password')
            user = Developer.objects.filter(devename=username, password=password).first()
            if user:
                request.session['deve_id'] = user.deveId
                # response = redirect(reverse('home'))
                response = HttpResponseRedirect(next)
                response.set_cookie("userId", user.deveId)
                response.set_cookie("username", username)
                response.set_cookie("password", password)
                return response
            else:
                print('用户名或密码错误')
                messages.success(request, "用户名或密码错误!")
                return redirect(reverse('develogin'))
        else:
            print(form.errors.get_json_data())
            messages.success(request, "用户名或密码错误!")
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
            messages.success(request, "注册成功，请登录！")
            return redirect(reverse('login'))
        else:
            errors = form.errors
            print(errors)
            messages.success(request, "填写信息无效！")
            return redirect(reverse('register'))
class deveregisterView(View):
    def get(self, request):
        data = {
            "title": "deveregister"
        }
        return render(request, 'dev_register.html', context=data)
    def post(self, request):
        form = deveregisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "注册成功，请登录！")
            return redirect(reverse('develogin'))
        else:
            messages.success(request, "填写信息无效！")
            return redirect(reverse('deveregister'))

def uploadfile(request):
    if request.method == 'GET':
        filename = request.GET.get('modelFile')
        userid = request.GET.get('userId')
        probid = request.GET.get('chId')
        devel = Developer.objects.get(pk=userid)
        prob = Challenge.objects.get(pk=int(probid))
        path = MEDIA_ROOT + filename
        size = os.path.getsize('/home/ubuntu/' + filename)
        with open('/home/ubuntu/' + filename, 'r') as f:
            SolutionFile.objects.create(file=InMemoryUploadedFile(f, None, filename, None, size, None, None),
                                        name=filename, size=size, path=path, auther=devel, problem=prob)
        messages.success(request, '上传成功！')
        return redirect(reverse('home'))
    if request.method == 'POST':
        taskId = request.GET.get('taskId', '')
        form = uploadForm(request.POST, request.FILES)
        deveId = request.session.get('deve_id')
        devel = Developer.objects.get(pk=deveId)
        prob = Challenge.objects.get(pk=int(taskId))
        if form.is_valid():
            file = request.FILES.get('file')
            name = str(file)
            size = len(file)
            path = MEDIA_ROOT+name
            SolutionFile.objects.create(file=file, name=name, size=size, path=path, auther=devel, problem=prob)
            messages.success(request, '上传成功！')
            return redirect(reverse('home'))
        else:
            messages.success(request, "填写信息无效！")
            return redirect(reverse('home'))
def score(request):
    if request.method == 'POST':
        file = request.FILES.get('csvfile')
        taskId = request.POST.get('taskId')
        ans = pd.read_csv(taskId +'/ans_submission.csv').values
        getfile = pd.read_csv(file).values
        num = ans.shape[0]
        for i in range(0, num):
            if ans[i][1] >= 0.5:
                ans[i][1] = 1
            else:
                ans[i][1] = 0
        y = list(ans[:, 1])
        score = roc_auc_score(y, getfile[:, 1])
        return HttpResponse(score)

def pred_tech(request):
    if request.method == "POST":
        title = request.POST.get('title')
        req = request.POST.get('details')
        pre_tec = pre_technology(title, req)
        tec = ''
        for i in pre_tec:
            tec += i
            tec += ' '
        return HttpResponse(tec)