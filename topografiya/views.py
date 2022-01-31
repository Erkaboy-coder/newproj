from django.shortcuts import render,redirect
from .models import Branch, PdoWork, Worker, Order, Object, History, ProgramWork, ProgramWorkForm, \
    ProgramWorkFormTable1, ProgramWorkFormTable2
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django import template
from django.contrib.auth.decorators import login_required
from pyvirtualdisplay import Display
import pdfkit
from django.db.models import Q

from django.core import serializers

# Create your views here.
@login_required(login_url='/signin')
def index(request):
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()

    context = {'objects': objects, 'objects_pdo': objects_pdo}
    return render(request, 'index.html', context)

def pdoworks(request):
    pdoworks = PdoWork.objects.filter(status=0).filter(~Q(status_recive=2))
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()

    context = {'pdoworks': pdoworks,'objects':objects,'objects_pdo':objects_pdo}
    return render(request, 'leader/pdo_works.html', context)

def allworks(request):
    pdoworks = PdoWork.objects.filter(status=0)
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()
    context = {'pdoworks': pdoworks,'objects':objects,'objects_pdo':objects_pdo}
    return render(request, 'leader/all_works.html', context)

def program_works_leader(request):
    new_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=0).all()
    checking_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=1).all()
    rejected_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=2).all()
    less_time_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=3).all()
    aggreed_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=4).all()


    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()

    context = {'objects': objects, 'objects_pdo': objects_pdo, 'new_ones': new_ones, 'checking_ones': checking_ones,
               'rejected_ones': rejected_ones, 'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones}
    # print(objects)
    return render(request, 'leader/program_works.html', context)

def program_work_form(request,id):

    object = Object.objects.filter(id=id).first()
    order = Order.objects.filter(object=object.id).first()
    workers = Worker.objects.filter(branch=object.pdowork.branch)

    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()

    context = {'object': object, 'order': order, 'workers': workers, 'objects': objects, 'objects_pdo': objects_pdo}
    return render(request, 'leader/program_work_form.html', context)

def program_work_form_edit(request,id):

    object = Object.objects.filter(id=id).first()
    form = ProgramWorkForm.objects.filter(programwork__object=id).first()
    formtable1 = ProgramWorkFormTable1.objects.filter(programworkform=form).first()
    formtable2 = ProgramWorkFormTable2.objects.filter(programworkform=form).first()

    order = Order.objects.filter(object=object.id).first()
    workers = Worker.objects.filter(branch=object.pdowork.branch)

    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()

    context = {'object': object, 'order': order, 'workers': workers, 'objects': objects, 'objects_pdo': objects_pdo, 'form': form, 'formtable1':formtable1,'formtable2':formtable2}
    return render(request, 'leader/program_work_form_edit.html', context)

def program_work_form_store(request):
    if request.method == 'POST':
        object = request.POST.get('object_id')
        a0 = request.POST.get('a0')
        a1_1 = request.POST.get('a1_1')
        a1_2 = request.POST.get('a1_2')
        a1_3 = request.POST.get('a1_3')

        a2 = request.POST.get('a2')
        a3 = request.POST.get('a3')
        a4 = request.POST.get('a4')
        a5 = request.POST.get('a5')
        a6 = request.POST.get('a6')
        a7 = request.POST.get('a7')

        # jadval_1
        a7_1_1 = request.POST.get('a7_1_1')
        a7_1_2 = request.POST.get('a7_1_2')
        a7_1_3 = request.POST.get('a7_1_3')
        a7_1_4 = request.POST.get('a7_1_4')
        a7_1_5 = request.POST.get('a7_1_5')
        # jadval_1

        a7_2 = request.POST.get('a7_2')
        a7_3 = request.POST.get('a7_3')
        a7_4 = request.POST.get('a7_4')

        a8 = request.POST.get('a8')
        a8_1 = request.POST.get('a8_1')
        a9_1 = request.POST.get('a9_1')

        # jadval_2
        a9_2_1 = request.POST.get('a9_2_1')
        a9_2_2 = request.POST.get('a9_2_2')
        a9_2_3 = request.POST.get('a9_2_3')
        a9_2_4 = request.POST.get('a9_2_4')
        a9_2_5 = request.POST.get('a9_2_5')
        a9_2_6 = request.POST.get('a9_2_6')
        a9_2_7 = request.POST.get('a9_2_7')
        # jadval_2

        a9_3 = request.POST.get('a9_3')
        a9_4 = request.POST.get('a9_4')

        a10 = request.POST.get('a10')
        a11 = request.POST.get('a11')
        a12 = request.POST.get('a12')

        program_work_creator = request.POST.get('program_work_creator')

        programwork = ProgramWork.objects.filter(object=object).first()
        programwork.status = 1
        programwork.save()
        # status  = 1 bu tekshiruvga yuborilgan

        programworkform = ProgramWorkForm(programwork=programwork, a0=a0, a1_1=a1_1, a1_2=a1_2, a1_3=a1_3, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7=a7, a7_2=a7_2,
                                        a7_3=a7_3, a7_4=a7_4, a8=a8, a8_1=a8_1, a9_1=a9_1, a9_3=a9_3, a9_4=a9_4, a10=a10, a11=a11, a12=a12, program_work_creator=program_work_creator)
        programworkform.save()

        programworkformtable1 = ProgramWorkFormTable1(programworkform=programworkform, a7_1_1=a7_1_1, a7_1_2=a7_1_2, a7_1_3=a7_1_3, a7_1_4=a7_1_4, a7_1_5=a7_1_5)
        programworkformtable1.save()

        programworkformtable2 = ProgramWorkFormTable2(programworkform=programworkform, a9_2_1=a9_2_1, a9_2_3=a9_2_3, a9_2_4=a9_2_4, a9_2_5=a9_2_5, a9_2_6=a9_2_6, a9_2_7=a9_2_7)
        programworkformtable2.save()


        messages.success(request, "Ish tekshiruvga yuborildi !")
        return HttpResponseRedirect('/program_works_leader')

def history_program_work(request):
    pdoworks = PdoWork.objects.filter(status=0)
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()

    context = {'pdoworks': pdoworks,'objects':objects,'objects_pdo':objects_pdo}
    return render(request, 'leader/history_program_work.html', context)

def worker_new_works(request):
    # status_recive = 1 is started work but not recived by worker
    worker_new_works = Object.objects.filter(pdowork__status_recive=1).all()
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()


    context = {'worker_new_works': worker_new_works,'objects':objects, 'objects_pdo':objects_pdo}
    return render(request, 'worker/worker_new_works.html', context)

def polevoy_works(request):
    # status_recive = 1 is started work but not recived by worker
    worker_new_works = Object.objects.filter(pdowork__status_recive=2).all()

    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()
    context = {'worker_new_works': worker_new_works,'objects':objects, 'objects_pdo':objects_pdo}
    return render(request, 'worker/polevoy_works.html', context)


def show_work(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('work_id')
        work = Object.objects.filter(pdowork__pk=id)
        pdowork = PdoWork.objects.filter(id=work.first().pdowork.id)

        return JsonResponse({'work': list(work.values()), 'pdowork': list(pdowork.values())}, safe=False)
    else:
        return HttpResponse(0)

def recive_work(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('data-id')
        print(id)
        worker_full_name= data.get('worker-id')

        object = Object.objects.filter(id=id).first()
        object.worker_ispolnitel=worker_full_name
        object.save()

        order = Order.objects.filter(object=object.id).first()
        order.order_receiver = worker_full_name
        order.save()

        pdoworks=PdoWork.objects.filter(id=object.pdowork_id).first()
        pdoworks.status_recive = 2
        # status_recive = 2 is worker recieved work
        pdoworks.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)


def order_to_pdf(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('data-id')
        object = Object.objects.filter(id=id).first()

        # print(work.first().pdowork.id)
        # pdowork = PdoWork.objects.filter(id=work.first().pdowork.id)
        order = Order.objects.filter(object=object.id).first()

        context = '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Title</title>
                        <style>
                            li{
                                padding: 5px;
                            }
                            li{
                            font-size:18px;
                            }

                        </style>
                </head>
                <body>
                <h2 style="text-align: center;margin-top: 55px">ПРЕДПИСАНИЕ на выполнение топографо-геодезических работ</h2>
                <br>
                <ol>''';

        context += '<li>Должность, Ф.И.О. исполнителя' + object.pdowork.customer_info + ' </li>';
        context += '<li>Наименование объекта ' + object.pdowork.object_name + '</li>';
        context += '<li>Местоположение объекта ' + object.pdowork.object_address + '</li>';
        context += '<li>Заказчик ' + object.pdowork.customer + '</li>';
        context += '<li>Виды и объемы работ ' + object.pdowork.work_type + '</li>';
        context += '<li>Сроки выполнения работ ' + object.pdowork.work_term + '</li>';
        context += '<li>Исходные данные, система координат и высот, использование материалов работ прошлых лет ' + order.info + '</li>';
        context += '<li>Метод создания геодезического и (или) съемочного обоснования, закрепление пунктов, точек ' + order.method_creation + '</li>';
        context += '<li>Метод создания геодезического и (или) съемочного обоснования, закрепление пунктов, точекМетод выполнения топографической съемки. Технические требования и технология выполнения работ ' + order.method_fill + '</li>';
        context += '<li>Съемка инженерно-подземных коммуникаций ' + order.syomka + '</li>';
        context += '<li>Особые требования ' + order.requirements + '</li>';
        context += '<li>Поверки геодезических инструментов ' + order.item_check + '</li>';
        context += '<li>Методы и программы уравнивания ' + order.adjustment_methods + '</li>';
        context += '<li>Перечень предоставляемых материалов ' + order.list_of_materials + '</li>';
        context += '<li>Перечень предоставляемых материалов ' + order.list_of_materials + '</li>';
        context += ''' <li>Приложение
                        <ol>
                            <li>Копия технического задания;</li>
                        <li>Графическое приложение.</li>
                    </ol>
                    </li>''';

        context += '<p>Предписание составил: ' + order.order_creator + ' </p>';
        context += '''</ol>
                </body>
                </html>''';

        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
            'orientation': 'Landscape',
        }
        # display = Display(visible=0, size=(500, 500)).start()
        pdfkit.from_string(context, 'topografiya/static/files/file.pdf', options)

        response = HttpResponse(data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="order.pdf"'
        return response
    else:
        return HttpResponse(0)

def show_pdowork(request,id):
    pdowork = PdoWork.objects.filter(id=id).first()
    workers=Worker.objects.filter(branch=pdowork.branch)
    context = {'pdowork': pdowork, 'workers': workers}
    return render(request, 'leader/show_pdowork.html', context)

def edit_pdowork(request,id):

    pdowork = PdoWork.objects.filter(id=id).filter(status_recive=1).first()
    workers=Worker.objects.filter(branch=pdowork.branch)
    order = Order.objects.filter(object__pdowork=pdowork).first()
    object=Object.objects.filter(pdowork=pdowork).first()
    context = {'pdowork': pdowork, 'workers': workers, 'order': order,'object':object}
    return render(request, 'leader/edit_pdowork.html', context)

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
        is_programwork = request.POST.get('is_programwork')

        pdowork = PdoWork.objects.filter(id=pdowork).first()
        pdowork.status_recive=1
        # status_recive = 1 is started work but not recived by worker
        pdowork.save()

        object = Object(pdowork=pdowork, worker_leader=order_creator, isset_programwork=is_programwork)
        object.save()

        order = Order(object=object,info=info,method_creation=method_creation,method_fill=method_fill,syomka=syomka,requirements=requirements,item_check=item_check,
                     list_of_materials=list_of_materials,adjustment_methods=adjustment_methods,type_of_sirie=type_of_sirie,order_creator=order_creator)
        order.save()
        print(is_programwork)

        if is_programwork == 'True':
            programm_work = ProgramWork(object=object, status=0)
            programm_work.save()

        history = History(user_id=order_creator, status=1, object=object, comment="Yangi obekt ish jarayoniga yuborildi")
        # status=1 work started by leader
        history.save()
        # messages.error(request, "Ish boshlandi ichi qabul qilishini kuting !")
        return HttpResponseRedirect('/pdoworks/')

    else:
        messages.error(request, "Bunday foydalanuvchi mavjud emas !")
        return HttpResponseRedirect('/')


def edit_pdowork_changes(request):
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
        worker_ispolnitel = request.POST.get('worker_ispolnitel')

        pdowork = request.POST.get('pdowork')
        worker_id = request.POST.get('worker_id')
        object_id = request.POST.get('object_id')
        is_programwork = request.POST.get('is_programwork')
        object = Object.objects.filter(id=object_id).first()
        object.pdowork=object.pdowork
        object.worker_leader=worker_id
        object.isset_programwork=is_programwork
        object.worker_ispolnitel=worker_ispolnitel
        object.save()

        order=Order.objects.filter(object=object).first()

        order.object=object
        order.info=info
        order.method_creation=method_creation
        order.method_fill=method_fill
        order.syomka=syomka
        order.requirements=requirements
        order.item_check=item_check
        order.list_of_materials=list_of_materials
        order.adjustment_methods=adjustment_methods
        order.type_of_sirie=type_of_sirie
        order.order_creator=order_creator
        order.save()

        program_work = ProgramWork.objects.filter(object=object_id).first()
        if is_programwork == 'True':
            if not program_work:
                programm_work = ProgramWork(object=object, status=0)
                programm_work.save()
        elif is_programwork == 'False':
            if program_work:
                program_work.delete()

        history = History(user_id=worker_id, status=7, object=object)
        # status=7 work updated
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
