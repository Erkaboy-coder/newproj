from django.shortcuts import render,redirect
from topografiya.models import Branch,PdoWork,Worker,Order,Object
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django import template
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/signin')
def index(request):
    context = {}
    return render(request, 'index.html', context)

def pdoworks(request):
    pdoworks = PdoWork.objects.filter(status=0)
    context = {'pdoworks': pdoworks}
    return render(request, 'leader/pdo_works.html', context)

def show_pdowork(request,id):

    pdowork = PdoWork.objects.filter(id=id).first()
    workers=Worker.objects.filter(branch=pdowork.branch)

    context = {'pdowork':pdowork,'workers':workers}
    return render(request, 'leader/show_pdowork.html', context)

def start(request):
    if request.method == 'POST':
        info = request.POST.get('info')
        method_creation = request.POST.get('method_creation')
        method_fill = request.POST.get('method_fill')
        syomka = request.POST.get('syomka')
        requirements = request.POST.get('requirements')
        item_check = request.POST.get('item_check')
        list_of_materials = request.POST.get('list_of_materials')
        adjustment_methods = request.POST.get('adjustment_methods')
        type_of_sirie = request.POST.get('type_of_sirie')
        order_creator = request.POST.get('order_creator')

        pdowork = request.POST.get('pdowork')
        worker_id = request.POST.get('worker_id')
        is_programwork = request.POST.get('is_programwork')

        pdowork = PdoWork.objects.filter(id=pdowork).first()
        pdowork.status_recive=1
        # status_recive = 1 is started work but not recived by worker
        pdowork.save()

        object=Object(pdowork=pdowork,worker_leader=worker_id, isset_programwork=is_programwork)
        object.save()

        order=Order(object=object.id,info=info,method_creation=method_creation,method_fill=method_fill,syomka=syomka,requirements=requirements,item_check=item_check,
                     list_of_materials=list_of_materials,adjustment_methods=adjustment_methods,type_of_sirie=type_of_sirie,order_creator=order_creator)
        order.save()

        history = History(user_id=worker_id,status=1,object=object)
        # status=1 work started by leader
        history.save()
        # messages.error(request, "Ish boshlandi ichi qabul qilishini kuting !")
        return HttpResponseRedirect('/pdoworks/')

    else:
        messages.error(request, "Bunday foydalanuvchi mavjud emas !")
        return HttpResponseRedirect('/')



def signin(request):
    content={}
    return render(request,'login.html',content)

def login(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=login, password=password)
        if user is not None:
            profile = Worker.objects.filter(user=user).first()
            if profile.permission:
                dj_login(request,user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "Sizga ruhsat berilmagan ! Kutishingizni so'raymiz ! Adminga murojat qiling !")
                return HttpResponseRedirect('/')

        else:
            messages.error(request, "Bunday foydalanuvchi mavjud emas !")
            return HttpResponseRedirect('/')
    else:
        messages.error(request, "Bunday foydalanuvchi mavjud emas !")
        return HttpResponseRedirect('/')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
