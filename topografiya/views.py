from django.shortcuts import render,redirect
from topografiya.models import Branch, PdoWork, Worker, Order, Object, History,ProgramWork
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django import template
from django.contrib.auth.decorators import login_required
from pyvirtualdisplay import Display
import pdfkit

from django.core import serializers

# Create your views here.
@login_required(login_url='/signin')
def index(request):
    objects = Object.objects.filter(pdowork__status_recive=1).all()
    objects_pdo = Object.objects.filter(pdowork__status_recive=0).all()
    context = {'objects': objects, 'objects_pdo': objects_pdo}
    return render(request, 'index.html', context)

def pdoworks(request):
    pdoworks = PdoWork.objects.filter(status=0)
    context = {'pdoworks': pdoworks}
    return render(request, 'leader/pdo_works.html', context)

def allworks(request):
    pdoworks = PdoWork.objects.filter(status=0)
    context = {'pdoworks': pdoworks}
    return render(request, 'leader/all_works.html', context)

def program_works(request):
    context = {}
    return render(request, 'leader/program_works.html', context)

def program_work_form(request):
    context = {}
    return render(request, 'leader/program_work_form.html', context)

def history_program_work(request):
    pdoworks = PdoWork.objects.filter(status=0)
    context = {'pdoworks': pdoworks}
    return render(request, 'leader/history_program_work.html', context)

def worker_new_works(request):
    # status_recive = 1 is started work but not recived by worker
    worker_new_works = Object.objects.filter(pdowork__status_recive=1).all()
    context = {'worker_new_works': worker_new_works}
    return render(request, 'worker/worker_new_works.html', context)

def show_work(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('work_id')

        work = Object.objects.filter(pdowork__pk=id)
        # print(work.first().pdowork.id)
        pdowork = PdoWork.objects.filter(id=work.first().pdowork.id)

        order = Order.objects.filter(object=work.first().id).first()

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

        context += '<li>Должность, Ф.И.О. исполнителя'+pdowork.first().customer_info+' </li>';
        context +=  '<li>Наименование объекта '+pdowork.first().object_name+'</li>';
        context += '<li>Местоположение объекта '+pdowork.first().object_address+'</li>';
        context += '<li>Заказчик '+pdowork.first().customer+'</li>';
        context += '<li>Виды и объемы работ '+pdowork.first().work_type+'</li>';
        context += '<li>Сроки выполнения работ '+pdowork.first().work_term+'</li>';
        context += '<li>Исходные данные, система координат и высот, использование материалов работ прошлых лет '+order.info+'</li>';
        context += '<li>Метод создания геодезического и (или) съемочного обоснования, закрепление пунктов, точек '+order.method_creation+'</li>';
        context += '<li>Метод создания геодезического и (или) съемочного обоснования, закрепление пунктов, точекМетод выполнения топографической съемки. Технические требования и технология выполнения работ '+order.method_fill+'</li>';
        context += '<li>Съемка инженерно-подземных коммуникаций '+order.syomka+'</li>';
        context += '<li>Особые требования '+order.requirements+'</li>';
        context += '<li>Поверки геодезических инструментов '+order.item_check+'</li>';
        context += '<li>Методы и программы уравнивания '+order.adjustment_methods+'</li>';
        context += '<li>Перечень предоставляемых материалов '+order.list_of_materials+'</li>';
        context += '<li>Перечень предоставляемых материалов '+order.list_of_materials+'</li>';
        context += ''' <li>Приложение
                        <ol>
                            <li>Копия технического задания;</li>
                        <li>Графическое приложение.</li>
                    </ol>
                    </li>''';

        context +='<p>Предписание составил: '+order.order_creator+' </p>';
        context +='''</ol>
                </body>
                </html>''';

        options = {
            'page-size': 'A5',
            'encoding': "UTF-8",
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
            'orientation': 'Landscape',
        }
        # display = Display(visible=0, size=(500, 500)).start()
        pdfkit.from_string(context, 'topografiya/static/files/file.pdf', options)

        work = PdoWork.objects.filter(status_recive=1).values()

        return JsonResponse({'work': list(work.values()), 'pdowork': list(pdowork.values())}, safe=False)
    else:
        return HttpResponse(0)

def recive_work(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('data-id')

        return HttpResponse(1)
    else:
        return HttpResponse(0)


# def ilova_to_pdf(request):
#     if request.method == 'POST':
#         data = request.POST
#         id = data.get('work_id')
#
#         work = Object.objects.filter(pdowork__pk=id)
#         # print(work.first().pdowork.id)
#         pdowork = PdoWork.objects.filter(id=work.first().pdowork.id)
#
#         order = Order.objects.filter(object=work.first().id).first()
#
#         context = '''
#                 <!DOCTYPE html>
#                 <html lang="en">
#                 <head>
#                     <meta charset="UTF-8">
#                     <title>Title</title>
#                         <style>
#                             li{
#                                 padding: 5px;
#                             }
#                             li{
#                             font-size:18px;
#                             }
#
#                         </style>
#                 </head>
#                 <body>
#                 <h2 style="text-align: center;margin-top: 55px">ПРЕДПИСАНИЕ на выполнение топографо-геодезических работ</h2>
#                 <br>
#                 <ol>''';
#
#         context += '<li>Должность, Ф.И.О. исполнителя' + pdowork.first().customer_info + ' </li>';
#         context += '<li>Наименование объекта ' + pdowork.first().object_name + '</li>';
#         context += '<li>Местоположение объекта ' + pdowork.first().object_address + '</li>';
#         context += '<li>Заказчик ' + pdowork.first().customer + '</li>';
#         context += '<li>Виды и объемы работ ' + pdowork.first().work_type + '</li>';
#         context += '<li>Сроки выполнения работ ' + pdowork.first().work_term + '</li>';
#         context += '<li>Исходные данные, система координат и высот, использование материалов работ прошлых лет ' + order.info + '</li>';
#         context += '<li>Метод создания геодезического и (или) съемочного обоснования, закрепление пунктов, точек ' + order.method_creation + '</li>';
#         context += '<li>Метод создания геодезического и (или) съемочного обоснования, закрепление пунктов, точекМетод выполнения топографической съемки. Технические требования и технология выполнения работ ' + order.method_fill + '</li>';
#         context += '<li>Съемка инженерно-подземных коммуникаций ' + order.syomka + '</li>';
#         context += '<li>Особые требования ' + order.requirements + '</li>';
#         context += '<li>Поверки геодезических инструментов ' + order.item_check + '</li>';
#         context += '<li>Методы и программы уравнивания ' + order.adjustment_methods + '</li>';
#         context += '<li>Перечень предоставляемых материалов ' + order.list_of_materials + '</li>';
#         context += '<li>Перечень предоставляемых материалов ' + order.list_of_materials + '</li>';
#         context += ''' <li>Приложение
#                         <ol>
#                             <li>Копия технического задания;</li>
#                         <li>Графическое приложение.</li>
#                     </ol>
#                     </li>''';
#
#         context += '<p>Предписание составил: ' + order.order_creator + ' </p>';
#         context += '''</ol>
#                 </body>
#                 </html>''';
#
#         options = {
#             'page-size': 'A5',
#             'encoding': "UTF-8",
#             'margin-top': '0.2in',
#             'margin-right': '0.2in',
#             'margin-bottom': '0.2in',
#             'margin-left': '0.2in',
#             'orientation': 'Landscape',
#         }
#         # display = Display(visible=0, size=(500, 500)).start()
#         pdfkit.from_string(context, 'topografiya/static/files/file.pdf', options)
#
#         response = HttpResponse(data, content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="lots.xlsx"'
#         return response
#     else:
#         return HttpResponse(0)

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
        worker_ispolnitel = request.POST.get('worker_ispolnitel')

        pdowork = request.POST.get('pdowork')
        worker_id = request.POST.get('worker_id')
        is_programwork = request.POST.get('is_programwork')

        pdowork = PdoWork.objects.filter(id=pdowork).first()
        pdowork.status_recive=1
        # status_recive = 1 is started work but not recived by worker
        pdowork.save()

        object = Object(pdowork=pdowork, worker_leader=worker_id, isset_programwork=is_programwork,worker_ispolnitel=worker_ispolnitel)
        object.save()

        order = Order(object=object,info=info,method_creation=method_creation,method_fill=method_fill,syomka=syomka,requirements=requirements,item_check=item_check,
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

        history = History(user_id=worker_id,status=7,object=object)
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
