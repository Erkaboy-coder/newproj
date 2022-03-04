from django.shortcuts import render,redirect
from .models import Branch, PdoWork, Worker, Order, Object, History, ProgramWork, ProgramWorkForm, \
    ProgramWorkFormTable1, ProgramWorkFormTable2, WorkerObject, ProgramWorkReject, SirieFiles, PoyasitelniyForm, \
    PoyasitelniyFormTable1, PoyasitelniyFormTable2, PoyasitelniyFormTable3, PoyasitelniyFormTable4, AktPolevoyForm, \
    AktPolovoyTable1, AktPolovoyTable2, AktPolovoyTable3, AktPolovoyTable4, AktPolovoyTable5, AktPolovoyTable6, \
    AktPolovoyTable7, AktPolovoyTable8, PolevoyWorkReject, AktKomeralForm, KameralWorkReject, LeaderKomeralWorkReject, \
    Report, ReportReject, ProgramWorkFiles,Lines,Polygons,Points
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django import template
from django.contrib.auth.decorators import login_required
from pyvirtualdisplay import Display
import pdfkit
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
from django.core import serializers

from django.core import serializers

# Create your views here.

def counter():
    count = {}
    count['new_workers_pdo'] = PdoWork.objects.filter(status_recive=0).all().count()
    # count['new_works_worker'] = PdoWork.objects.filter(status_recive=1).all().count()

    count['new_works_geodezis'] = ProgramWork.objects.filter(status=1).all().count()
    count['new_program_works_leader'] = ProgramWork.objects.filter(status=0).all().count()
    count['new_polevoy_works_leader'] = WorkerObject.objects.filter(status=1).all().count()
    count['new_komeral_works_leader'] = AktKomeralForm.objects.filter(status=0).all().count()

    count['geodezis_komeral_works_to_check'] = WorkerObject.objects.filter(status_geodezis_komeral=1).all().count()
    count['leader_komeral_works_to_check'] = WorkerObject.objects.filter(status_geodezis_komeral=2).all().count()

    count['reports_oogd'] = Report.objects.filter(status=0).all().count()
    count['new_geodezis_reports'] = Report.objects.filter(status=1).all().count()

    count['new_ogogd_printer_works'] = WorkerObject.objects.filter(status_geodezis_komeral=4).filter(object__isset_programwork=False).all().count()


    return count

def new_work_counter(request):
    count_works = {}
    count_works['new_works_worker'] = Object.objects.filter(pdowork__status_recive=1).filter(worker_ispolnitel=request.user.profile.full_name).all().count()
    count_works['new_field_works'] = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(object__worker_ispolnitel=request.user.profile.full_name).filter(status=0).all().count()
    count_works['worker_komeral_works'] = AktKomeralForm.objects.filter(status=2).filter(object__worker_ispolnitel=request.user.profile.full_name).all().count()
    return count_works

@login_required(login_url='/signin')
def index(request):
    context = {'count': counter(),'count_works': new_work_counter(request)}
    return render(request, 'index.html', context)

def pdoworks(request):
    pdoworks = PdoWork.objects.filter(status=0).filter(~Q(status_recive=2))
    context = {'pdoworks': pdoworks,'count': counter()}
    return render(request, 'leader/pdo_works.html', context)

def save_order(request):
    if request.method == 'POST':
        data = request.POST
        isset_programwork = data.get('isset_programwork')
        info = data.get('info')
        worker_ispolnitel = data.get('worker_ispolnitel')
        method_creation = data.get('method_creation')
        method_fill = data.get('method_fill')
        syomka = data.get('syomka')
        requirements = data.get('requirements')
        item_check = data.get('item_check')
        adjustment_methods = data.get('adjustment_methods')
        list_of_materials = data.get('list_of_materials')
        type_of_sirie = data.get('type_of_sirie')
        order_creator = data.get('order_creator')
        order_receiver = data.get('order_receiver')
        pdowork_id = data.get('pdowork_id')

        pdowork = PdoWork.objects.filter(id=pdowork_id).first()

        object = Object(pdowork=pdowork, worker_leader=order_creator, isset_programwork=isset_programwork,
                        worker_ispolnitel=worker_ispolnitel)
        object.save()

        order = Order(object=object, info=info, method_creation=method_creation, method_fill=method_fill, syomka=syomka,
                      requirements=requirements, item_check=item_check,
                      list_of_materials=list_of_materials, adjustment_methods=adjustment_methods,
                      type_of_sirie=type_of_sirie, order_creator=order_creator,order_receiver=order_receiver)
        order.save()


        return HttpResponse(1)
    else:
        return HttpResponse(0)


def allworks(request):
    pdoworks = PdoWork.objects.filter(status=0)
    context = {'pdoworks': pdoworks, 'count': counter(),'count_works': new_work_counter(request)}
    return render(request, 'leader/all_works.html', context)

def program_works_leader(request):
    new_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=0).all()
    checking_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=1).all()
    rejected_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=2).all()
    less_time_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=3).all()
    aggreed_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=4).all()
    rejecteds = ProgramWorkReject.objects.all()

    context = {'new_ones': new_ones, 'checking_ones': checking_ones,
               'rejected_ones': rejected_ones, 'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones,'rejecteds':rejecteds, 'count': counter()}
    # print(objects)
    return render(request, 'leader/program_works/program_works.html', context)

def program_work_form(request,id):

    object = ProgramWork.objects.filter(object=id).first()
    order = Order.objects.filter(object=object.object.id).first()
    workers = Worker.objects.filter(branch=object.object.pdowork.branch).filter(status=0)

    form = ProgramWorkForm.objects.filter(programwork__object=id).first()
    formtable1 = ProgramWorkFormTable1.objects.filter(programworkform=form).first()
    formtable2 = ProgramWorkFormTable2.objects.filter(programworkform=form).first()
    files = ProgramWorkFiles.objects.filter(programworkform=form).first()

    context = {'object': object, 'order': order, 'workers': workers,'count': counter(),'form':form, 'formtable1': formtable1, 'formtable2': formtable2,'files':files}
    return render(request, 'leader/program_works/program_work_form.html', context)

def program_work_form_edit(request,id):

    object = Object.objects.filter(id=id).first()
    form = ProgramWorkForm.objects.filter(programwork__object=id).first()
    formtable1 = ProgramWorkFormTable1.objects.filter(programworkform=form).first()
    formtable2 = ProgramWorkFormTable2.objects.filter(programworkform=form).first()
    files = ProgramWorkFiles.objects.filter(programworkform=form).first()
    rejects = ProgramWorkReject.objects.filter(programowork=form.programwork).all()

    order = Order.objects.filter(object=id).first()
    workers = Worker.objects.filter(branch=object.pdowork.branch).filter(status=0)


    context = {'object': object, 'order': order, 'workers': workers, 'form': form, 'rejects':rejects,'files': files,
               'formtable1':formtable1,'formtable2':formtable2,'count': counter()}
    return render(request, 'leader/program_works/program_work_form_edit.html', context)

def program_work_form_re_sent_to_check(request,id):

    object = Object.objects.filter(id=id).first()
    form = ProgramWorkForm.objects.filter(programwork__object=id).first()
    formtable1 = ProgramWorkFormTable1.objects.filter(programworkform=form).first()
    formtable2 = ProgramWorkFormTable2.objects.filter(programworkform=form).first()
    files = ProgramWorkFiles.objects.filter(programworkform=form).first()
    rejects = ProgramWorkReject.objects.filter(programowork=form.programwork).all()

    order = Order.objects.filter(object=id).first()
    workers = Worker.objects.filter(branch=object.pdowork.branch).filter(status=0)


    context = {'object': object, 'order': order, 'workers': workers, 'form': form, 'rejects':rejects,'files': files,
               'formtable1':formtable1,'formtable2':formtable2,'count': counter()}
    return render(request, 'leader/program_works/program_work_form_re_sent_to_check.html', context)


def program_work_save_edits(request,id):
    if request.method == 'POST':
        a0 = request.POST.get('a0')
        a1_1 = request.POST.get('a1_1')
        a1_2 = request.POST.get('a1_2')
        a1_3 = request.POST.get('a1_3')

        a2 = request.POST.get('a2')
        a3 = request.POST.get('a3')
        a4 = request.POST.get('a4')
        a5 = request.POST.get('a5')
        a6 = request.POST.get('a6')

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

        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        file3 = request.FILES.get('file3')
        file4 = request.FILES.get('file4')
        file5 = request.FILES.get('file5')
        file6 = request.FILES.get('file6')
        file7 = request.FILES.get('file7')

        program_work_creator = request.POST.get('program_work_creator')

        object = Object.objects.filter(id=id).first()
        programwork=ProgramWork.objects.filter(object=object.id).first()

        form = ProgramWorkForm.objects.filter(programwork=programwork).first()
        form.programwork=programwork
        form.a0=a0
        form.a1_1=a1_1
        form.a1_2 = a1_2
        form.a1_3 = a1_3
        form.a2 = a2
        form.a3 = a3
        form.a4 = a4
        form.a5 = a5
        form.a6=a6
        form.a7_2=a7_2
        form.a7_3=a7_3
        form.a7_4=a7_4
        form.a8=a8
        form.a8_1=a8_1
        form.a9_1=a9_1
        form.a9_3=a9_3
        form.a9_4=a9_4
        form.a10=a10
        form.a11=a11
        form.a12=a12
        form.program_work_creator=program_work_creator
        form.save()

        formtable1 = ProgramWorkFormTable1.objects.filter(programworkform=form).first()
        formtable1.programworkform=form
        formtable1.a7_1_1=a7_1_1
        formtable1.a7_1_2=a7_1_2
        formtable1.a7_1_3=a7_1_3
        formtable1.a7_1_4=a7_1_4
        formtable1.a7_1_5=a7_1_5
        formtable1.save()

        formtable2 = ProgramWorkFormTable2.objects.filter(programworkform=form).first()
        formtable2.programworkform=form
        formtable2.a9_2_1=a9_2_1
        formtable2.a9_2_2=a9_2_2
        formtable2.a9_2_3=a9_2_3
        formtable2.a9_2_4=a9_2_4
        formtable2.a9_2_5=a9_2_5
        formtable2.a9_2_6=a9_2_6
        formtable2.a9_2_7=a9_2_7
        formtable2.save()

        files = ProgramWorkFiles.objects.filter(programworkform=form).first()
        if file1:
            files.file1 = file1
        else:
            files.file1=files.file1

        if file2:
            files.file2 = file2
        else:
            files.file2 = files.file2

        if file3:
            files.file3 = file3
        else:
            files.file3 = files.file3

        if file4:
            files.file4 = file4
        else:
            files.file4 = files.file4

        if file5:
            files.file1 = file5
        else:
            files.file5 = files.file5

        if file6:
            files.file6 = file6
        else:
            files.file6 = files.file6


        if file7:
            files.file6 = file7
        else:
            files.file7 = files.file7

        files.save()


        history = History(object=object, status=26, comment="Ishchi dastur o'zgarishlari saqlandi", user_id = program_work_creator)
        # status=26 ishchi dastur o'zgarishlari saqlandi
        history.save()


        return redirect('program_work_form', id=programwork.object.id)

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
        # files
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        file3 = request.FILES.get('file3')
        file4 = request.FILES.get('file4')
        file5 = request.FILES.get('file5')
        file6 = request.FILES.get('file6')
        file7 = request.FILES.get('file7')

        program_work_creator = request.POST.get('program_work_creator')

        programwork = ProgramWork.objects.filter(object=object).first()
        # programwork.status = 1
        # programwork.save()
        # status  = 1 bu tekshiruvga yuborilgan

        programworkform = ProgramWorkForm(programwork=programwork, a0=a0, a1_1=a1_1, a1_2=a1_2, a1_3=a1_3, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7_2=a7_2,
                                        a7_3=a7_3, a7_4=a7_4, a8=a8, a8_1=a8_1, a9_1=a9_1, a9_3=a9_3, a9_4=a9_4, a10=a10, a11=a11, a12=a12, program_work_creator=program_work_creator)
        programworkform.save()

        programworkformtable1 = ProgramWorkFormTable1(programworkform=programworkform, a7_1_1=a7_1_1, a7_1_2=a7_1_2, a7_1_3=a7_1_3, a7_1_4=a7_1_4, a7_1_5=a7_1_5)
        programworkformtable1.save()

        programworkformtable2 = ProgramWorkFormTable2(programworkform=programworkform, a9_2_1=a9_2_1, a9_2_2=a9_2_2, a9_2_3=a9_2_3, a9_2_4=a9_2_4, a9_2_5=a9_2_5, a9_2_6=a9_2_6, a9_2_7=a9_2_7)
        programworkformtable2.save()

        programwork_file = ProgramWorkFiles(programworkform=programworkform,file1=file1,file2=file2,file3=file3,file4=file4,file5=file5,file6=file6,file7=file7)
        programwork_file.save()


        # messages.success(request, "O'zgarishlar saqlandi !")
        return redirect('program_work_form', id=programwork.object.id)

def sent_to_check_programwork(request):
    if request.method == 'POST':
        data = request.POST
        object_id = data.get('object_id')
        worker = data.get('worker')
        programwork = ProgramWork.objects.filter(object=object_id).first()
        programwork.status = 1
        programwork.save()
        # status  = 1 bu tekshiruvga yuborilgan


        history = History(object=programwork.object, status=27, comment="Ishchi dasturi tekshiruvga yuborildi", user_id=worker)
        history.save()

        return HttpResponse(1)

    else:

        return HttpResponse(0)


def history_program_work(request):
    pdoworks = PdoWork.objects.filter(status=0)

    context = {'pdoworks': pdoworks, 'count': counter()}
    return render(request, 'leader/history_program_work.html', context)

def leader_polevoy_works(request):
    # status_recive = 1 is started work but not recived by worker
    # new_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=0).all() # yangi kelgan
    checking_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=1).all() # dala nazorati muhokama jarayonida
    rejected_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=2).all() # qaytarilgan ishlar
    less_time_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=3).all() # muddati kam qolgan ishlar
    aggreed_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=4).all() # tasdiqlangan ishlar
    rejecteds = PolevoyWorkReject.objects.all()
    context = {'checking_ones': checking_ones, 'rejected_ones': rejected_ones,
               'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones,'count': counter(),'rejecteds': rejecteds}
    return render(request, 'leader/polevoy/polevoy_works.html', context)

def checking_polevoy_works(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()

    pdowork = Object.objects.filter(id=id).first()
    siriefiles = SirieFiles.objects.filter(workerobject=workerobject).first()
    order = Order.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=workerobject.object.id).first()
    work = AktPolevoyForm.objects.filter(object=id).first()
    work_table1 = AktPolovoyTable1.objects.filter(aktpolovoy=work).first()
    work_table2 = AktPolovoyTable2.objects.filter(aktpolovoy=work).first()
    work_table3 = AktPolovoyTable3.objects.filter(aktpolovoy=work).first()
    work_table4 = AktPolovoyTable4.objects.filter(aktpolovoy=work).first()
    work_table5 = AktPolovoyTable5.objects.filter(aktpolovoy=work).first()
    work_table6 = AktPolovoyTable6.objects.filter(aktpolovoy=work).first()
    work_table7 = AktPolovoyTable7.objects.filter(aktpolovoy=work).first()
    work_table8 = AktPolovoyTable8.objects.filter(aktpolovoy=work).first()

    rejects = PolevoyWorkReject.objects.filter(workerobject=workerobject).all()
    
    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(), 'siriefiles': siriefiles,'order':order,
               'work_table1':work_table1, 'work_table2':work_table2, 'work_table3':work_table3, 'work_table4':work_table4, 'work_table5':work_table5,
                'work_table6':work_table6, 'work_table7':work_table7, 'work_table8':work_table8,'work':work,'rejects':rejects,'programwork':programwork
               }

    return render(request, 'leader/polevoy/checking_polevoy_works.html', context)

def save_akt_polevoy(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')
        array=data.get('array')
        array1=data.get('array1')
        array2=data.get('array2')
        array3=data.get('array3')
        array4=data.get('array4')
        array5=data.get('array5')
        array6=data.get('array6')
        array7=data.get('array7')
        array8=data.get('array8')

        d={}
        object=Object.objects.filter(id=work_id).first()
        j=0
        j1=0
        j2=0
        j3=0
        j4=0
        j5=0
        j6=0
        j7=0
        j8=0

        d = {'object': object}
        for i in array.split(','):
            j=j+1
            d['a'+str(j)]=i
        k=AktPolevoyForm.objects.create(**d)

        b = {'aktpolovoy': k}
        for i in array1.split(','):
            j1 = j1 + 1
            b['a1_' + str(j1)] = i

        e = {'aktpolovoy': k}
        for i in array2.split(','):
            j2 = j2 + 1
            e['a2_' + str(j2)] = i

        f = {'aktpolovoy': k}
        for i in array3.split(','):
            j3 = j3 + 1
            f['a3_' + str(j3)] = i

        g = {'aktpolovoy': k}
        for i in array4.split(','):
            j4 = j4 + 1
            g['a4_' + str(j4)] = i

        h = {'aktpolovoy': k}
        for i in array5.split(','):
            j5 = j5 + 1
            h['a5_' + str(j5)] = i

        p = {'aktpolovoy': k}
        for i in array6.split(','):
            j6 = j6 + 1
            p['a6_' + str(j6)] = i

        m = {'aktpolovoy': k}
        for i in array7.split(','):
            j7 = j7 + 1
            m['a7_' + str(j7)] = i

        o = {'aktpolovoy': k}
        for i in array8.split(','):
            j8 = j8 + 1
            o['a8_' + str(j8)] = i

        AktPolovoyTable1.objects.create(**b)
        AktPolovoyTable2.objects.create(**e)
        AktPolovoyTable3.objects.create(**f)
        AktPolovoyTable4.objects.create(**g)
        AktPolovoyTable5.objects.create(**h)
        AktPolovoyTable6.objects.create(**p)
        AktPolovoyTable7.objects.create(**m)
        AktPolovoyTable8.objects.create(**o)


        history = History(object=object, status=11, comment="Dala nazoratida akt yaratildi",user_id=worker)
        history.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def edit_akt_polevoy(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')
        array=data.get('array')
        array1=data.get('array1')
        array2=data.get('array2')
        array3=data.get('array3')
        array4=data.get('array4')
        array5=data.get('array5')
        array6=data.get('array6')
        array7=data.get('array7')
        array8=data.get('array8')

        d={}
        object=Object.objects.filter(id=work_id).first()
        j=0
        j1=0
        j2=0
        j3=0
        j4=0
        j5=0
        j6=0
        j7=0
        j8=0

        d = {'object': object}
        for i in array.split(','):
            j=j+1
            d['a'+str(j)]=i
        k = AktPolevoyForm.objects.filter(object=object).update(**d)
        form = AktPolevoyForm.objects.filter(object=work_id).first()
        b = {'aktpolovoy': form}
        for i in array1.split(','):
            j1 = j1 + 1
            b['a1_' + str(j1)] = i

        e = {'aktpolovoy': form}
        for i in array2.split(','):
            j2 = j2 + 1
            e['a2_' + str(j2)] = i

        f = {'aktpolovoy': form}
        for i in array3.split(','):
            j3 = j3 + 1
            f['a3_' + str(j3)] = i

        g = {'aktpolovoy': form}
        for i in array4.split(','):
            j4 = j4 + 1
            g['a4_' + str(j4)] = i

        h = {'aktpolovoy': form}
        for i in array5.split(','):
            j5 = j5 + 1
            h['a5_' + str(j5)] = i

        p = {'aktpolovoy': form}
        for i in array6.split(','):
            j6 = j6 + 1
            p['a6_' + str(j6)] = i

        m = {'aktpolovoy': form}
        for i in array7.split(','):
            j7 = j7 + 1
            m['a7_' + str(j7)] = i

        o = {'aktpolovoy': form}
        for i in array8.split(','):
            j8 = j8 + 1
            o['a8_' + str(j8)] = i

        AktPolovoyTable1.objects.filter(aktpolovoy_id=form.pk).update(**b)
        AktPolovoyTable2.objects.filter(aktpolovoy_id=form.pk).update(**e)
        AktPolovoyTable3.objects.filter(aktpolovoy_id=form.pk).update(**f)
        AktPolovoyTable4.objects.filter(aktpolovoy_id=form.pk).update(**g)
        AktPolovoyTable5.objects.filter(aktpolovoy_id=form.pk).update(**h)
        AktPolovoyTable6.objects.filter(aktpolovoy_id=form.pk).update(**p)
        AktPolovoyTable7.objects.filter(aktpolovoy_id=form.pk).update(**m)
        AktPolovoyTable8.objects.filter(aktpolovoy_id=form.pk).update(**o)


        history = History(object=object, status=12, comment="Dala nazoratida akt o'zgartirildi",user_id=worker)
        history.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def send_to_kameral(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')

        workerobject = WorkerObject.objects.filter(object=work_id).first()
        workerobject.status = 4
        workerobject.save()

        kameral = AktKomeralForm(object=workerobject.object)
        kameral.save()


        history = History(object=workerobject.object, status=13, comment="Ish dala nazoratidan tasdiqlandi",user_id=worker)
        history.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)
# def deny_polevoy(request):
#     if request.method == 'POST':
#         data = request.POST
#         work_id = data.get('work_id')
#         worker = data.get('worker')
#
#         workerobject = WorkerObject.objects.filter(object=work_id).first()
#         workerobject.status = 4
#         workerobject.save()
#
#
#         history = History(object=workerobject.object, status=13, comment="Ish dala nazoratidan tasdiqlandi",user_id=worker)
#         history.save()
#         return HttpResponse(1)
#     else:
#         return HttpResponse(0)

def deny_polevoy(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')
        reason = data.get('reason')
        reason_file =request.FILES.get('reason_file')

        workerobject = WorkerObject.objects.filter(object=work_id).first()
        workerobject.status = 2
        workerobject.save()

        object_id = Object.objects.filter(id=work_id).first()

        reject = PolevoyWorkReject(workerobject=workerobject, file=reason_file, reason=reason)
        reject.save()

        history = History(object=object_id, status=15, comment="Rad etildi", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def leader_komeral_works(request):
    # status_recive = 1 is started work but not recived by worker
    new_ones = AktKomeralForm.objects.filter(status=0).all()  # komeral nazoratiga kelgan ishlar
    checking_ones = AktKomeralForm.objects.filter(status=1).all()  # dala nazorati muhokama jarayonida
    rejected_ones = AktKomeralForm.objects.filter(status=2).all()  # qaytarilgan ishlar
    less_time_ones = AktKomeralForm.objects.filter(status=3).all()  # muddati kam qolgan ishlar
    aggreed_ones =AktKomeralForm.objects.filter(status=4).all()  # tasdiqlangan ishlar
    rejecteds = KameralWorkReject.objects.all()

    context = {'checking_ones': checking_ones, 'rejected_ones': rejected_ones,
               'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones, 'count': counter(),'new_ones':new_ones,
               'rejecteds': rejecteds}
    return render(request, 'leader/komeral/komeral_works.html', context)

def leader_komeral_checking(request):
    # status_recive = 1 is started work but not recived by worker
    checking_ones = WorkerObject.objects.filter(status_geodezis_komeral=1).all()  # dala nazorati muhokama jarayonida
    rejected_ones = WorkerObject.objects.filter(status_geodezis_komeral=2).all()  # qaytarilgan ishlar
    less_time_ones = WorkerObject.objects.filter(status_geodezis_komeral=3).all()  # muddati kam qolgan ishlar
    aggreed_ones =WorkerObject.objects.filter(status_geodezis_komeral=4).all()  # tasdiqlangan ishlar
    rejecteds = LeaderKomeralWorkReject.objects.all()

    context = {'checking_ones': checking_ones, 'rejected_ones': rejected_ones,
               'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones, 'count': counter(),'rejecteds': rejecteds}
    return render(request, 'leader/head_komeral/komeral_works.html', context)

def checking_komeral_works(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()
    siriefiles = SirieFiles.objects.filter(workerobject=workerobject).first()
    order = Order.objects.filter(object=id).first()
    work = AktKomeralForm.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    rejects = KameralWorkReject.objects.filter(workerobject=workerobject.object).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(), 'siriefiles': siriefiles, 'order':order,'work':work, 'rejects':rejects, 'programwork': programwork}

    return render(request, 'leader/komeral/checking_komeral_works.html', context)


def show_komeral_work(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()
    siriefiles = SirieFiles.objects.filter(workerobject=workerobject).first()
    order = Order.objects.filter(object=id).first()

    work = AktKomeralForm.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    rejects = KameralWorkReject.objects.filter(workerobject=workerobject.object).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(), 'siriefiles': siriefiles, 'order':order, 'work':work, 'rejects':rejects,'programwork':programwork}

    return render(request, 'leader/komeral/show_komeral_work.html', context)

def rejected_komeral_works(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = AktKomeralForm.objects.filter(object=id).first()

    rejects = KameralWorkReject.objects.filter(workerobject=workerobject.object).all()
    programwork = ProgramWork.objects.filter(object=id).first()
    
    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(),'order':order,'work':work,'rejects':rejects,'programwork': programwork}

    return render(request, 'leader/komeral/rejected_komeral_works.html', context)

def save_akt_komeral(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')
        array=data.get('array')

        d={}
        object=Object.objects.filter(id=work_id).first()
        j=0
        d = {'object': object, 'status': 4}
        for i in array.split(','):
            j=j+1
            d['a'+str(j)]=i
        AktKomeralForm.objects.filter(object=work_id).update(**d)

        # workerobject=WorkerObject.objects.filter(object=work_id).first()
        # workerobject.status_geodezis_komeral=1
        # workerobject.save()

        # history = History(object=object, status=17, comment="Komeral nazorat tasdiqlandi",user_id=worker)
        # history.save()
        history = History(object=object, status=28, comment="Komeral nazorat aktisi saqlandi", user_id=worker)
        history.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def sent_to_check_akt(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')
        array=data.get('array')

        d={}
        object=Object.objects.filter(id=work_id).first()
        j=0
        d = {'object': object, 'status': 4}
        for i in array.split(','):
            j=j+1
            d['a'+str(j)]=i
        AktKomeralForm.objects.filter(object=work_id).update(**d)

        workerobject=WorkerObject.objects.filter(object=work_id).first()
        workerobject.status_geodezis_komeral=1
        workerobject.save()

        history = History(object=object, status=17, comment="Komeral nazorat tasdiqlandi",user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def deny_komeral(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')
        reason = data.get('reason')
        reason_file =request.FILES.get('reason_file')

        workerobject = AktKomeralForm.objects.filter(object=work_id).first()
        workerobject.status = 2
        workerobject.save()

        object_id = Object.objects.filter(id=work_id).first()

        reject = KameralWorkReject(workerobject=workerobject.object, file=reason_file, reason=reason)
        reject.save()

        history = History(object=object_id, status=15, comment="Rad etildi", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def show_komeral_checking_leader(request,id):
    work = WorkerObject.objects.filter(object=id).first()
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    rejects = LeaderKomeralWorkReject.objects.filter(object=id)
    context = {'objects': objects, 'work': work, 'objects_pdo': objects_pdo,
               'sirie_type': sirie_type,
               'file': sirie_files, 'count': counter(), 'rejects': rejects}

    return render(request, 'leader/head_komeral/show_komeral_work.html', context)

def leader_rejected_komeral_works(request,id):
    work = WorkerObject.objects.filter(object=id).first()
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    rejects = LeaderKomeralWorkReject.objects.filter(object=id)
    context = {'objects': objects, 'work':work,'objects_pdo': objects_pdo, 'sirie_type':sirie_type,
               'file': sirie_files,'count': counter(),'rejects':rejects}
    return render(request, 'leader/head_komeral/rejected_komeral_works.html', context)

def leader_akt_form_edit(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()
    siriefiles = SirieFiles.objects.filter(workerobject=workerobject).first()
    order = Order.objects.filter(object=id).first()

    work = AktPolevoyForm.objects.filter(object=id).first()
    work_table1 = AktPolovoyTable1.objects.filter(aktpolovoy=work).first()
    work_table2 = AktPolovoyTable2.objects.filter(aktpolovoy=work).first()
    work_table3 = AktPolovoyTable3.objects.filter(aktpolovoy=work).first()
    work_table4 = AktPolovoyTable4.objects.filter(aktpolovoy=work).first()
    work_table5 = AktPolovoyTable5.objects.filter(aktpolovoy=work).first()
    work_table6 = AktPolovoyTable6.objects.filter(aktpolovoy=work).first()
    work_table7 = AktPolovoyTable7.objects.filter(aktpolovoy=work).first()
    work_table8 = AktPolovoyTable8.objects.filter(aktpolovoy=work).first()

    rejects = PolevoyWorkReject.objects.filter(workerobject=workerobject).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(), 'siriefiles': siriefiles,'order':order,
               'work_table1':work_table1, 'work_table2':work_table2, 'work_table3':work_table3, 'work_table4':work_table4, 'work_table5':work_table5,
                'work_table6':work_table6, 'work_table7':work_table7, 'work_table8':work_table8,'work':work,'rejects':rejects
               }

    return render(request, 'leader/head_komeral/akt_polevoy.html', context)



def leader_akt_komeral_form_edit(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()
    siriefiles = SirieFiles.objects.filter(workerobject=workerobject).first()
    order = Order.objects.filter(object=id).first()

    work = AktKomeralForm.objects.filter(object=id).first()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(), 'siriefiles': siriefiles, 'order':order, 'work':work}

    return render(request, 'leader/head_komeral/akt_komeral.html', context)

def re_send_to_check_komeral(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work-id')
        worker = data.get('worker')

        workerobject = WorkerObject.objects.filter(object=work_id).first()
        workerobject.status_geodezis_komeral = 1
        workerobject.save()

        history = History(object=workerobject.object, status=19, comment="Ish geodezis komeral nazoratiga qayta yuborildi",user_id=worker)
        history.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

# leader


# worker
def worker_new_works(request):
    # status_recive = 1 is started work but not recived by worker
    worker_new_works = Object.objects.filter(pdowork__status_recive=1).filter(worker_ispolnitel=request.user.profile.full_name).all()

    context = {'worker_new_works': worker_new_works, 'count': counter(),'count_works': new_work_counter(request)}
    return render(request, 'worker/worker_new_works.html', context)

def polevoy_works(request):
    # status_recive = 1 is started work but not recived by worker
    new_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=0).filter(object__worker_ispolnitel=request.user.profile.full_name).all() # yangi kelgan
    checking_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=1).all() # muhokama jarayonida
    rejected_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=2).all() # qaytarilgan ishlar
    less_time_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=3).all() # muddati kam qolgan ishlar
    aggreed_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=4).all() # tasdiqlangan ishlar
    rejects = PolevoyWorkReject.objects.all()
    context = {'worker_new_works': worker_new_works,'new_ones': new_ones, 'checking_ones': checking_ones, 'rejected_ones': rejected_ones,
               'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones,'count': counter(),'rejects': rejects,'count_works': new_work_counter(request)}
    return render(request, 'worker/polevoy_works.html', context)

def worker_komeral_works(request):
    # status_recive = 1 is started work but not recived by worker
    checking_ones = AktKomeralForm.objects.filter(status=0).all()  # dala nazorati muhokama jarayonida
    rejected_ones = AktKomeralForm.objects.filter(status=2).all()  # qaytarilgan ishlar
    less_time_ones = AktKomeralForm.objects.filter(status=3).all()  # muddati kam qolgan ishlar
    aggreed_ones =AktKomeralForm.objects.filter(status=4).all()  # tasdiqlangan ishlar
    rejecteds = KameralWorkReject.objects.all()

    context = {'worker_new_works': worker_new_works, 'checking_ones': checking_ones, 'rejected_ones': rejected_ones,
               'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones, 'count': counter(),'count_works': new_work_counter(request),'rejecteds': rejecteds}
    return render(request, 'worker/komeral/komeral_works.html', context)

def show_rejected_komeral_works(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()

    aktkomeral = AktKomeralForm.objects.filter(object=id).first()

    rejects = KameralWorkReject.objects.filter(workerobject=workerobject.object).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(),'order':order,'work':work,'rejects':rejects,'sirie_type':sirie_type,
               'file': sirie_files,'aktkomeral':aktkomeral,'count_works': new_work_counter(request)}

    return render(request, 'worker/komeral/rejected_komeral_works.html', context)

def send_to_check_komeral(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work-id')
        worker = data.get('worker')

        workerobject = AktKomeralForm.objects.filter(object=work_id).first()
        print(workerobject)
        workerobject.status=0
        workerobject.save()


        history = History(object=workerobject.object, status=16, comment="Ish komeral nazorat tekshiruviga qayta yuborildi",user_id=worker)
        history.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def polevoy_work_doing(request,id):
    work = WorkerObject.objects.filter(object=id).first()
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    rejects = PolevoyWorkReject.objects.filter(workerobject=work)
    programwork = ProgramWork.objects.filter(object=id).first()

    context = {'worker_new_works': worker_new_works, 'objects': objects, 'work':work,'objects_pdo': objects_pdo, 'sirie_type':sirie_type,
               'file': sirie_files,'count': counter(),'rejects':rejects,'programwork': programwork,'count_works': new_work_counter(request)}
    return render(request, 'worker/polevoy_work_doing.html', context)

def send_to_check_polevoy(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work-id')
        print(work_id)
        worker = data.get('worker')

        workerobject = WorkerObject.objects.filter(id=work_id).first()
        print(workerobject)
        workerobject.status=1
        workerobject.save()


        history = History(object=workerobject.object, status=7, comment="Ish dala nazorati tekshiruvga yuborildi",user_id=worker)
        history.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def save_sirie_files(request):
    if request.method == 'POST':
        id = request.POST.get('work-id')
        worker = request.POST.get('worker')

        file1_1 =request.FILES.get('file1_1')
        file1_2 =request.FILES.get('file1_2')
        file1_3 =request.FILES.get('file1_3')
        file1_4 =request.FILES.get('file1_4')
        file1_5 =request.FILES.get('file1_5')
        file1_6 =request.FILES.get('file1_6')
        file1_7 =request.FILES.get('file1_7')
        file1_8 =request.FILES.get('file1_8')
        file1_9 =request.FILES.get('file1_9')
        file1_10 =request.FILES.get('file1_10')
        file1_11 =request.FILES.get('file1_11')

        file2_1 = request.FILES.get('file2_1')
        file2_2 = request.FILES.get('file2_2')
        file2_3 = request.FILES.get('file2_3')
        file2_4 = request.FILES.get('file2_4')
        file2_5 = request.FILES.get('file2_5')
        file2_6 = request.FILES.get('file2_6')
        file2_7 = request.FILES.get('file2_7')

        file3_1 = request.FILES.get('file3_1')
        file3_2 = request.FILES.get('file3_2')
        file3_3 = request.FILES.get('file3_3')
        file3_4 = request.FILES.get('file3_4')
        file3_5 = request.FILES.get('file3_5')
        file3_6 = request.FILES.get('file3_6')
        file3_7 = request.FILES.get('file3_7')
        file3_8 = request.FILES.get('file3_8')
        file3_9 = request.FILES.get('file3_9')
        file3_10 = request.FILES.get('file3_10')

        object = WorkerObject.objects.filter(id=id).first()

        workerobject = SirieFiles(workerobject=object, file1_1=file1_1,file1_2=file1_2,file1_3=file1_3,file1_4=file1_4,file1_5=file1_5,file1_6=file1_6,file1_7=file1_7,
        file1_8=file1_8,file1_9=file1_9,file1_10=file1_10,file1_11=file1_11,file2_1=file2_1,file2_2=file2_2,file2_3=file2_3,file2_4=file2_4,file2_5=file2_5,
        file2_6=file2_6,file2_7=file2_7,file3_1=file3_1,file3_2=file3_2,file3_3=file3_3,file3_4=file3_4,file3_5=file3_5,file3_6=file3_6,file3_7=file3_7,file3_8=file3_8,
        file3_9=file3_9, file3_10=file3_10)
        workerobject.save()

        object_id = Object.objects.filter(id=object.object.id).first()
        aktkomeral = AktKomeralForm.objects.filter(object=object_id).first()

        history = History(object=object_id, status=7, comment="Dala nazoratiga sirie ma'lumotlari yuklandi", user_id=worker)
        history.save()

        if object.status_geodezis_komeral == 2:
            return redirect('leader_rejected_komeral_works', id=object_id.id)
        if aktkomeral:
            if aktkomeral.status == 2:
                return redirect('show_rejected_komeral_works', id=object_id.id)
            else:
                return redirect('polevoy_work_doing', id=object_id.id)
        else:
            return redirect('polevoy_work_doing', id=object_id.id)
        

    else:
        return HttpResponseRedirect('/')

def edit_sirie_files(request,id):
    if request.method == 'POST':
        worker = request.POST.get('worker')

        file1_1 =request.FILES.get('file1_1')
        file1_2 =request.FILES.get('file1_2')
        file1_3 =request.FILES.get('file1_3')
        file1_4 =request.FILES.get('file1_4')
        file1_5 =request.FILES.get('file1_5')
        file1_6 =request.FILES.get('file1_6')
        file1_7 =request.FILES.get('file1_7')
        file1_8 =request.FILES.get('file1_8')
        file1_9 =request.FILES.get('file1_9')
        file1_10 =request.FILES.get('file1_10')
        file1_11 =request.FILES.get('file1_11')

        file2_1 = request.FILES.get('file2_1')
        file2_2 = request.FILES.get('file2_2')
        file2_3 = request.FILES.get('file2_3')
        file2_4 = request.FILES.get('file2_4')
        file2_5 = request.FILES.get('file2_5')
        file2_6 = request.FILES.get('file2_6')
        file2_7 = request.FILES.get('file2_7')

        file3_1 = request.FILES.get('file3_1')
        file3_2 = request.FILES.get('file3_2')
        file3_3 = request.FILES.get('file3_3')
        file3_4 = request.FILES.get('file3_4')
        file3_5 = request.FILES.get('file3_5')
        file3_6 = request.FILES.get('file3_6')
        file3_7 = request.FILES.get('file3_7')
        file3_8 = request.FILES.get('file3_8')
        file3_9 = request.FILES.get('file3_9')
        file3_10 = request.FILES.get('file3_10')

        object = WorkerObject.objects.filter(id=id).first()

        workerobject = SirieFiles.objects.filter(workerobject=id).first()
        workerobject.workerobject=object

        if file1_1:
            workerobject.file1_1=file1_1
        else:
            workerobject.file1_1=workerobject.file1_1

        if file1_2:
            workerobject.file1_2=file1_2
        else:
            workerobject.file1_2=workerobject.file1_2

        if file1_3:
            workerobject.file1_3 = file1_3
        else:
            workerobject.file1_3 = workerobject.file1_3

        if file1_4:
            workerobject.file1_4 = file1_4
        else:
            workerobject.file1_4 = workerobject.file1_4

        if file1_5:
            workerobject.file1_5 = file1_5
        else:
            workerobject.file1_5 = workerobject.file1_5


        if file1_6:
            workerobject.file1_6 = file1_6
        else:
            workerobject.file1_6 = workerobject.file1_6


        if file1_7:
            workerobject.file1_7 = file1_7
        else:
            workerobject.file1_7 = workerobject.file1_7


        if file1_8:
            workerobject.file1_8 = file1_8
        else:
            workerobject.file1_8 = workerobject.file1_8


        if file1_9:
            workerobject.file1_9 = file1_9
        else:
            workerobject.file1_9 = workerobject.file1_9


        if file1_10:
            workerobject.file1_10 = file1_10
        else:
            workerobject.file1_10 = workerobject.file1_10


        if file1_11:
            workerobject.file1_11 = file1_11
        else:
            workerobject.file1_11 = workerobject.file1_11


        if file2_1:
            workerobject.file2_1 = file2_1
        else:
            workerobject.file2_1 = workerobject.file2_1


        if file2_2:
            workerobject.file2_2 = file2_2
        else:
            workerobject.file2_2 = workerobject.file2_2


        if file2_3:
            workerobject.file2_3 = file2_3
        else:
            workerobject.file2_3 = workerobject.file2_3


        if file2_4:
            workerobject.file2_4 = file2_4
        else:
            workerobject.file2_4 = workerobject.file2_4


        if file2_5:
            workerobject.file2_5 = file2_5
        else:
            workerobject.file2_5 = workerobject.file2_5


        if file2_6:
            workerobject.file2_6 = file2_6
        else:
            workerobject.file2_6 = workerobject.file2_6


        if file2_7:
            workerobject.file2_7 = file2_7
        else:
            workerobject.file2_7 = workerobject.file2_7



        if file3_1:
            workerobject.file3_1 = file3_1
        else:
            workerobject.file3_1 = workerobject.file3_1

        if file3_2:
            workerobject.file3_2 = file3_2
        else:
            workerobject.file3_2 = workerobject.file3_2


        if file3_3:
            workerobject.file3_3 = file3_3
        else:
            workerobject.file3_3 = workerobject.file3_3


        if file3_4:
            workerobject.file3_4 = file3_4
        else:
            workerobject.file3_4 = workerobject.file3_4


        if file3_5:
            workerobject.file3_5 = file3_5
        else:
            workerobject.file3_5 = workerobject.file3_5


        if file3_6:
            workerobject.file3_6 = file3_6
        else:
            workerobject.file3_6 = workerobject.file3_6


        if file3_7:
            workerobject.file3_7 = file3_7
        else:
            workerobject.file3_7 = workerobject.file3_7


        if file3_8:
            workerobject.file3_8 = file3_8
        else:
            workerobject.file3_8 = workerobject.file3_8


        if file3_9:
            workerobject.file3_9 = file3_9
        else:
            workerobject.file3_9 = workerobject.file3_9


        if file3_10:
            workerobject.file3_10 = file3_10
        else:
            workerobject.file3_10 = workerobject.file3_10
        workerobject.save()

        object_id = Object.objects.filter(id=object.object.id).first()
        aktkomeral = AktKomeralForm.objects.filter(object=object_id).first()

        history = History(object=object_id, status=7, comment="Dala nazoratiga sirie ma'lumotlari yuklandi", user_id=worker)
        history.save()
        
        if object.status_geodezis_komeral == 2:
            return redirect('leader_rejected_komeral_works', id=object_id.id)
        if aktkomeral:
            if aktkomeral.status == 2:
                return redirect('show_rejected_komeral_works', id=object_id.id)
            else:
                return redirect('polevoy_work_doing', id=object_id.id)
        else:
            return redirect('polevoy_work_doing', id=object_id.id)
        

    else:
        return HttpResponseRedirect('/')

def store(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')

        b1 = data.get('b1')
        b2 = data.get('b2')
        b_1 = data.get('b_1')
        b_2 = data.get('b_2')
        b_3 = data.get('b_3')
        b3 = data.get('b3')
        b3_1 = data.get('b3_1')
        b4 = data.get('b4')
        b5 = data.get('b5')
        b6 = data.get('b6')
        b7 = data.get('b7')
        b8_1_1 = data.get('b8_1_1')
        b10 = data.get('b10')
        b11 = data.get('b11')
        b12 = data.get('b12')
        b13 = data.get('b13')
        b14 = data.get('b14')
        b15 = data.get('b15')
        b16_a = data.get('b16_a')
        b16_b = data.get('b16_b')

        b19 = data.get('b19')
        b19_1 = data.get('b19_1')
        b19_2 = data.get('b19_2')
        b20 = data.get('b20')
        b21 = data.get('b21')

        c_1 = data.get('c_1')
        c_2 = data.get('c_2')
        c_3 = data.get('c_3')
        c_4 = data.get('c_4')
        c_5 = data.get('c_5')
        c_6 = data.get('c_6')
        c_7 = data.get('c_7')
        c_8 = data.get('c_8')
        c_9 = data.get('c_9')
        c_10 = data.get('c_10')
        c_11 = data.get('c_11')
        c_12 = data.get('c_12')
        c_13 = data.get('c_13')
        c_14 = data.get('c_14')
        c_15 = data.get('c_15')
        c_16 = data.get('c_16')
        c_17 = data.get('c_17')
        c_18 = data.get('c_18')
        c_19 = data.get('c_19')
        c_20 = data.get('c_20')
        c_21 = data.get('c_21')
        c_22 = data.get('c_22')
        c_23 = data.get('c_23')
        c_24 = data.get('c_24')
        c_25 = data.get('c_25')
        c_26 = data.get('c_26')

        d_1 = data.get('d_1')
        d_2 = data.get('d_2')
        d_3 = data.get('d_3')
        d_4 = data.get('d_4')
        d_5 = data.get('d_5')
        d_6 = data.get('d_6')
        d_7 = data.get('d_7')
        d_8 = data.get('d_8')
        d_9 = data.get('d_9')
        d_10 = data.get('d_10')
        d_11 = data.get('d_11')
        d_12 = data.get('d_12')
        d_13 = data.get('d_13')

        b8_1 = data.get('b8_1')
        b8_2 = data.get('b8_2')
        b8_3 = data.get('b8_3')
        b8_4 = data.get('b8_4')

        b9_1 = data.get('b9_1')
        b9_2 = data.get('b9_2')
        b9_3 = data.get('b9_3')
        b9_4 = data.get('b9_4')

        b17_1 = data.get('b17_1')
        b17_2 = data.get('b17_2')
        b17_3 = data.get('b17_3')
        b17_4 = data.get('b17_4')
        b17_5 = data.get('b17_5')
        b17_6 = data.get('b17_6')
        b17_7 = data.get('b17_7')

        b18_1 = data.get('b18_1')
        b18_2 = data.get('b18_2')
        b18_3 = data.get('b18_3')
        b18_4 = data.get('b18_4')
        b18_5 = data.get('b18_5')

        workerobject=WorkerObject.objects.filter(id=work_id).first()

        form1 = PoyasitelniyForm(workerobject=workerobject, b1=b1, b2=b2, b_1=b_1, b_2=b_2,b_3=b_3, b3=b3, b3_1=b3_1, b4=b4, b5=b5, b6=b6,b7=b7,b8_1_1=b8_1_1,b10=b10,b11=b11,b12=b12
                                 ,b13=b13,b14=b14,b15=b15,b16_a=b16_a,b16_b=b16_b,b19=b19,b19_1=b19_1,b19_2=b19_2,b20=b20,b21=b21,c_1=c_1,c_2=c_2,c_3=c_3,c_4=c_4,c_5=c_5,c_6=c_6
                                 ,c_7=c_7,c_8=c_8,c_9=c_9,c_10=c_10,c_11=c_11,c_12=c_12,c_13=c_13,c_14=c_14,c_15=c_15,c_16=c_16,c_17=c_17,c_18=c_18,c_19=c_19
                                 ,c_20=c_20,c_21=c_21,c_22=c_22,c_23=c_23,c_24=c_24,c_25=c_25,c_26=c_26,d_1=d_1,d_2=d_2,d_3=d_3,d_4=d_4,d_5=d_5,d_6=d_6,d_7=d_7
                                 ,d_8=d_8,d_9=d_9,d_10=d_10,d_11=d_11,d_12=d_12,d_13=d_13)
        form1.save()

        form2=PoyasitelniyFormTable1(poyasitelniyform=form1,b8_1=b8_1,b8_2=b8_2,b8_3=b8_3,b8_4=b8_4)
        form2.save()

        form3 = PoyasitelniyFormTable2(poyasitelniyform=form1,b9_1=b9_1,b9_2=b9_2,b9_3=b9_3,b9_4=b9_4)
        form3.save()

        form4 = PoyasitelniyFormTable3(poyasitelniyform=form1,b17_1=b17_1,b17_2=b17_2,b17_3=b17_3,b17_4=b17_4,b17_5=b17_5,b17_6=b17_6,b17_7=b17_7)
        form4.save()

        form5 = PoyasitelniyFormTable4(poyasitelniyform=form1,b18_1=b18_1,b18_2=b18_2,b18_3=b18_3,b18_4=b18_4,b18_5=b18_5)
        form5.save()

        object_id = Object.objects.filter(id=workerobject.object.id).first()

        history = History(object=object_id, status=9, comment="Dala nazoratiga poyasitelniy formaga ma'lumot yuklandi",
                          user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def edit_poyasitelniy(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')

        b1 = data.get('b1')
        b2 = data.get('b2')
        b_1 = data.get('b_1')
        b_2 = data.get('b_2')
        b_3 = data.get('b_3')
        b3 = data.get('b3')
        b3_1 = data.get('b3_1')
        b4 = data.get('b4')
        b5 = data.get('b5')
        b6 = data.get('b6')
        b7 = data.get('b7')
        b8_1_1 = data.get('b8_1_1')
        b10 = data.get('b10')
        b11 = data.get('b11')
        b12 = data.get('b12')
        b13 = data.get('b13')
        b14 = data.get('b14')
        b15 = data.get('b15')
        b16_a = data.get('b16_a')
        b16_b = data.get('b16_b')

        b19 = data.get('b19')
        b19_1 = data.get('b19_1')
        b19_2 = data.get('b19_2')
        b20 = data.get('b20')
        b21 = data.get('b21')

        c_1 = data.get('c_1')
        c_2 = data.get('c_2')
        c_3 = data.get('c_3')
        c_4 = data.get('c_4')
        c_5 = data.get('c_5')
        c_6 = data.get('c_6')
        c_7 = data.get('c_7')
        c_8 = data.get('c_8')
        c_9 = data.get('c_9')
        c_10 = data.get('c_10')
        c_11 = data.get('c_11')
        c_12 = data.get('c_12')
        c_13 = data.get('c_13')
        c_14 = data.get('c_14')
        c_15 = data.get('c_15')
        c_16 = data.get('c_16')
        c_17 = data.get('c_17')
        c_18 = data.get('c_18')
        c_19 = data.get('c_19')
        c_20 = data.get('c_20')
        c_21 = data.get('c_21')
        c_22 = data.get('c_22')
        c_23 = data.get('c_23')
        c_24 = data.get('c_24')
        c_25 = data.get('c_25')
        c_26 = data.get('c_26')

        d_1 = data.get('d_1')
        d_2 = data.get('d_2')
        d_3 = data.get('d_3')
        d_4 = data.get('d_4')
        d_5 = data.get('d_5')
        d_6 = data.get('d_6')
        d_7 = data.get('d_7')
        d_8 = data.get('d_8')
        d_9 = data.get('d_9')
        d_10 = data.get('d_10')
        d_11 = data.get('d_11')
        d_12 = data.get('d_12')
        d_13 = data.get('d_13')

        b8_1 = data.get('b8_1')
        b8_2 = data.get('b8_2')
        b8_3 = data.get('b8_3')
        b8_4 = data.get('b8_4')

        b9_1 = data.get('b9_1')
        b9_2 = data.get('b9_2')
        b9_3 = data.get('b9_3')
        b9_4 = data.get('b9_4')

        b17_1 = data.get('b17_1')
        b17_2 = data.get('b17_2')
        b17_3 = data.get('b17_3')
        b17_4 = data.get('b17_4')
        b17_5 = data.get('b17_5')
        b17_6 = data.get('b17_6')
        b17_7 = data.get('b17_7')

        b18_1 = data.get('b18_1')
        b18_2 = data.get('b18_2')
        b18_3 = data.get('b18_3')
        b18_4 = data.get('b18_4')
        b18_5 = data.get('b18_5')

        workerobject=WorkerObject.objects.filter(id=work_id).first()

        form1 = PoyasitelniyForm.objects.filter(workerobject=workerobject).first()
        form1.workerobject=workerobject
        form1.b1=b1
        form1.b2=b2
        form1.b_1=b_1
        form1.b_2=b_2
        form1.b_3=b_3
        form1.b3=b3
        form1.b3_1=b3_1
        form1.b4=b4
        form1.b5=b5
        form1.b6=b6
        form1.b7=b7
        form1.b8_1_1=b8_1_1
        form1.b10=b10
        form1.b11=b11
        form1.b12=b12
        form1.b13=b13
        form1.b14=b14
        form1.b15=b15
        form1.b16_a=b16_a
        form1.b16_b=b16_b
        form1.b19=b19
        form1.b19_1=b19_1
        form1.b19_2=b19_2
        form1.b20=b20
        form1.b21=b21
        form1.c_1=c_1
        form1.c_2=c_2
        form1.c_3=c_3
        form1.c_4=c_4
        form1.c_5=c_5
        form1.c_6=c_6
        form1.c_7=c_7
        form1.c_8=c_8
        form1.c_9=c_9
        form1.c_10=c_10
        form1.c_11=c_11
        form1.c_12=c_12
        form1.c_13=c_13
        form1.c_14=c_14
        form1.c_15=c_15
        form1.c_16=c_16
        form1.c_17=c_17
        form1.c_18=c_18
        form1.c_19=c_19
        form1.c_20=c_20
        form1.c_21=c_21
        form1.c_22=c_22
        form1.c_23=c_23
        form1.c_24=c_24
        form1.c_25=c_25
        form1.c_26=c_26
        form1.d_1=d_1
        form1.d_2=d_2
        form1.d_3=d_3
        form1.d_4=d_4
        form1.d_5=d_5
        form1.d_6=d_6
        form1.d_7=d_7
        form1.d_8=d_8
        form1.d_9=d_9
        form1.d_10=d_10
        form1.d_11=d_11
        form1.d_12=d_12
        form1.d_13=d_13
        form1.save()

        form2=PoyasitelniyFormTable1.objects.filter(poyasitelniyform=form1).first()
        form2.poyasitelniyform=form1
        form2.b8_1=b8_1
        form2.b8_2=b8_2
        form2.b8_3=b8_3
        form2.b8_4=b8_4
        form2.save()

        form3 = PoyasitelniyFormTable2.objects.filter(poyasitelniyform=form1).first()
        form3.poyasitelniyform=form1
        form3.b9_1=b9_1
        form3.b9_2=b9_2
        form3.b9_3=b9_3
        form3.b9_4=b9_4
        form3.save()

        form4 = PoyasitelniyFormTable3.objects.filter(poyasitelniyform=form1).first()
        form4.poyasitelniyform = form1
        form4.b17_1=b17_1
        form4.b17_2=b17_2
        form4.b17_3=b17_3
        form4.b17_4=b17_4
        form4.b17_5=b17_5
        form4.b17_6=b17_6
        form4.b17_7=b17_7
        form4.save()

        form5 = PoyasitelniyFormTable4.objects.filter(poyasitelniyform=form1).first()
        form5.poyasitelniyform = form1
        form5.b18_1=b18_1
        form5.b18_2=b18_2
        form5.b18_3=b18_3
        form5.b18_4=b18_4
        form5.b18_5=b18_5
        form5.save()

        object_id = Object.objects.filter(id=workerobject.object.id).first()

        history = History(object=object_id, status=9, comment="Dala nazoratiga poyasitelniy formaga ma'lumot yuklandi",
                          user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)


def save_files(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('work-id')
        worker = data.get('worker')

        abris =request.FILES.get('abris')
        kroki =request.FILES.get('kroki')
        jurnal =request.FILES.get('jurnal')
        vidimes =request.FILES.get('vidimes')
        list =request.FILES.get('list')

        points = data.get('geometry_point')
        lines = data.get('geometry_line')
        polygons = data.get('geometry_polygon')

        object = WorkerObject.objects.filter(id=id).first()

        points_1 = Points.objects.filter(object=object.object).first()
        lines_1 = Lines.objects.filter(object=object.object).first()
        polygons_1 = Polygons.objects.filter(object=object.object).first()

        if points_1:
            points_1.object = object.object
            points_1.title = 'Edited points'
            points_1.points = GEOSGeometry(points)
            points_1.save()
        else:
            if points:
                points = Points(object=object.object, title='new points', points=GEOSGeometry(points))
                points.save()

        if lines_1:
            lines_1.object = object.object
            lines_1.title = 'Edited lines'
            lines_1.lines = GEOSGeometry(lines)
            lines_1.save()

        else:
            if lines:
                lines = Lines(object=object.object, title='new lines', lines=GEOSGeometry(lines))
                lines.save()

        if polygons_1:
            polygons_1.object = object.object
            polygons_1.title = 'Edited polygons'
            polygons_1.polygons = GEOSGeometry(polygons)
            polygons_1.save()

        else:
            if polygons:
                polygons = Polygons(object=object.object, title='new lines', polygons=GEOSGeometry(polygons))
                polygons.save()


        if abris:
            object.abris_file = abris
        else:
            object.abris_file = object.abris_file

        if kroki:
            object.kroki_file = kroki
        else:
            object.kroki_file = object.kroki_file


        if jurnal:
            object.jurnal_file = jurnal
        else:
            object.jurnal_file = object.jurnal_file

        if vidimes:
            object.vidimes_file = vidimes
        else:
            object.vidimes_file = object.vidimes_file

        if list:
            object.list_agreement_file = list
        else:
            object.list_agreement_file = object.list_agreement_file


        object.save()

        object_id = Object.objects.filter(id=object.object.id).first()

        history = History(object=object_id, status=8, comment="Dala nazoratiga fayl yuklandi", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def obj_data(request):
    id=request.POST.get('id')

    lines = Lines.objects.filter(object=id)
    points = Points.objects.filter(object=id)
    polygons = Polygons.objects.filter(object=id)

    test_data_p= serializers.serialize('geojson',points, geometry_field='points',fields=['points',])
    test_data_l= serializers.serialize('geojson',lines, geometry_field='lines',fields=['lines',])
    test_data_po= serializers.serialize('geojson',polygons, geometry_field='polygons',fields=['polygons',])
    return JsonResponse({'data1':test_data_p,'data2':test_data_l,'data3':test_data_po})

def object_poyasitelniy_form(request,id):
    work = WorkerObject.objects.filter(object=id).first()
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    form=PoyasitelniyForm.objects.filter(workerobject=work).first()
    form1=PoyasitelniyFormTable1.objects.filter(poyasitelniyform=form).first()
    form2=PoyasitelniyFormTable2.objects.filter(poyasitelniyform=form).first()
    form3=PoyasitelniyFormTable3.objects.filter(poyasitelniyform=form).first()
    form4=PoyasitelniyFormTable4.objects.filter(poyasitelniyform=form).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()
    context = {'worker_new_works': worker_new_works, 'objects': objects, 'work':work, 'objects_pdo': objects_pdo,'sirie_type':sirie_type,'count': counter(),
               'form':form, 'form1':form1, 'form2':form2, 'form3':form3, 'form4':form4,'count_works': new_work_counter(request),'aktkomeral':aktkomeral
               }
    return render(request, 'worker/object_poyasitelniy_form.html', context)

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
        worker_full_name= data.get('worker-id')

        object = Object.objects.filter(id=id).first()
        object.worker_ispolnitel=worker_full_name
        object.save()

        order = Order.objects.filter(object=object.id).first()
        order.order_receiver = worker_full_name
        order.save()

        pdoworks = PdoWork.objects.filter(id=object.pdowork_id).first()
        pdoworks.status_recive = 2
        # status_recive = 2 is worker recieved work
        pdoworks.save()

        workerobject = WorkerObject(object=object)
        workerobject.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def show_akt_polevoy_worker(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()
    siriefiles = SirieFiles.objects.filter(workerobject=workerobject).first()
    order = Order.objects.filter(object=id).first()
    worker = Worker.objects.filter()
    work = AktPolevoyForm.objects.filter(object=id).first()
    work_table1 = AktPolovoyTable1.objects.filter(aktpolovoy=work).first()
    work_table2 = AktPolovoyTable2.objects.filter(aktpolovoy=work).first()
    work_table3 = AktPolovoyTable3.objects.filter(aktpolovoy=work).first()
    work_table4 = AktPolovoyTable4.objects.filter(aktpolovoy=work).first()
    work_table5 = AktPolovoyTable5.objects.filter(aktpolovoy=work).first()
    work_table6 = AktPolovoyTable6.objects.filter(aktpolovoy=work).first()
    work_table7 = AktPolovoyTable7.objects.filter(aktpolovoy=work).first()
    work_table8 = AktPolovoyTable8.objects.filter(aktpolovoy=work).first()

    rejects = PolevoyWorkReject.objects.filter(workerobject=workerobject).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(), 'siriefiles': siriefiles,'order':order,
               'work_table1':work_table1, 'work_table2':work_table2, 'work_table3':work_table3, 'work_table4':work_table4, 'work_table5':work_table5,
                'work_table6':work_table6, 'work_table7':work_table7, 'work_table8':work_table8,'work':work,'rejects':rejects, 'count_works': new_work_counter(request)}

    return render(request, 'worker/komeral/akt_polevoy.html', context)

# worker

def order_to_pdf(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('data-id')
        object = Object.objects.filter(id=id).first()

        # print(work.first().pdowork.id)
        # pdowork = PdoWork.objects.filter(id=work.first().pdowork.id)
        order = Order.objects.filter(object=object.id).first()
        print(object.pdowork.tz)
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
                <h2 style="text-align: center;margin-top: 55px">ПРЕДПИСАНИЕ</h2>
                <p style='text-align: center'>на выполнение топографо-геодезических работ</p>
                <br>
                <ol>''';

        context += '<li>Должность, Ф.И.О. исполнителя ' + object.worker_ispolnitel + ' </li>';
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
        context += '<li>Метод топографической съемки ' + order.type_of_sirie + '</li>';
        context += ' <li>Приложение: <ol>'
        context += '<li><a href=http://0.0.0.0:1515/'+str(object.pdowork.tz)+'>Копия технического задания</a></li>';
        context += ' <li><a href=http://0.0.0.0:1515/'+str(object.pdowork.smeta)+'>Графическое приложение</a>.</li>';
        context += '</ol></li>';

        context += '<p>Предписание составил: ' + order.order_creator + ' </p>';
        context += '<p>Предписание получил: ' + object.worker_ispolnitel + ' </p>';
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
            'orientation': 'portrait',
            # landscape bu albomiy qiladi
        }
        # display = Display(visible=0, size=(500, 500)).start()
        pdfkit.from_string(context, 'topografiya/static/files/file.pdf', options)

        response = HttpResponse(data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="order.pdf"'
        return response
    else:
        return HttpResponse(0)

def doing_program_work_file(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('data-id')
        programwork = ProgramWork.objects.filter(id=id).first()
        form = ProgramWorkForm.objects.filter(programwork=programwork).first()
        programworkfile = ProgramWorkFiles.objects.filter(programworkform=form).first()
        programworktable1 = ProgramWorkFormTable1.objects.filter(programworkform=form).first()
        programworktable2 = ProgramWorkFormTable2.objects.filter(programworkform=form).first()

        # print(work.first().pdowork.id)
        # pdowork = PdoWork.objects.filter(id=work.first().pdowork.id)
        # order = Order.objects.filter(object=form.object.id).first()
        # order = Order.objects.filter(object=form.object.id).first()

        context = '''
        <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Title</title>
     <style>
        li {
            padding: 5px;
        }
        th,tr,table,td{
            border: 1px solid black
        }
        input{
                border: 0px solid;
                font-size:20px;
        }
        textarea{
            border: 0px solid;
        }
         body{
            font-size: 25px;
        }
    </style>
</head>

<body>

    <div style="padding: 100px">

        <h2 style="text-align: center;">ПРОГРАММА ТОПОГРАФО-ГЕОДЕЗИЧЕСКИХ РАБОТ</h2>
        <br>
        <p>По <span><input class="w-50 formact" name="a0" value="'''+str(form.a0)+'''" required type="text" placeholder="наименование объекта, его местоположение"></span> </p>
        <h5 style="text-align: center"><span class="badge rounded-pill badge-primary">1</span> ОБЩИЕ ДАННЫЕ</h5>
        <p>
            Основанием для производства работ послужило техническое задание, выданное
            <span><input class="w-50 m-b-5 formact" name="a1_1" value="'''+str(form.a1_1)+'''" type="text"></span>
            <br> Цель, назначение и объем проектируемых работ
            <span><input class="w-75 m-b-5 formact" required name="a1_2" value="'''+str(form.a1_2)+'''" type="text"></span> Дополнительные требования к выполнению геодезических работ
            <span><input class="w-75 m-b-5 formact" required name="a1_3" value="'''+str(form.a1_3)+'''" type="text"></span>
        </p>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary" style="text-align: center">2</span> КРАТКАЯ ФИЗИКО-ГЕОГРАФИЧЕСКАЯ ХАРАКТЕРИСТИКА РАЙОНА РАБОТ</p>
            <div class="col-sm-9">
                <p>'''+str(form.a2)+'''</p>
            </div>
        </div>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary">3</span> СВЕДЕНИЯ О СИСТЕМЕ КООРДИНАТ И ВЫСОТ</p>
            <div class="col-sm-9">
                <input class="form-control" name="a3" value="'''+str(form.a3)+'''" type="text" placeholder="">
            </div>
        </div>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary">4</span> ТОПОГРАФО-ГЕОДЕЗИЧЕСКАЯ ИЗУЧЕННОСТЬ РАЙОНА РАБОТ</p>
            <div class="col-sm-9">
                <p>'''+str(form.a4)+'''</p>
            </div>
        </div>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary">5</span> РАЗВИТИЕ ОПОРНОЙ ГЕОДЕЗИЧЕСКОЙ СЕТИ СГУЩЕНИЯ</p>
            <div class="col-sm-9">
                <p>'''+str(form.a5)+'''</p>
            </div>
        </div>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary">6</span> ПОСТРОЕНИЕ СЪЕМОЧНОГО ОБОСНОВАНИЯ</p>
            <div class="col-sm-9">
                <p>'''+str(form.a6)+'''</p>
            </div>
        </div>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary">7</span> ПРОИЗВОДСТВО ТОПОГРАФИЧЕСКИХ СЪЕМОК</p>
        </div>
        <div style="text-transform: lowercase;" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-warning">7.1</span> Вид, масштаб и объем съемки.</div>
        <div class="col-sm-12">
            <div class="card border-0">
                <div class="table-responsive">
                    <table class="table table-bordered" style="border: 1px solid black" id="childTable">
                        <thead class="bg-primary">
                            <tr style="border: 1px solid black">
                                <th scope="col">Наименование площадки, участка</th>
                                <th scope="col">Метод съемки</th>
                                <th scope="col">Масштаб съемки</th>
                                <th scope="col">Высота сечения рельефа, м</th>
                                <th scope="col">Объем</th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr>
                                <td><input class="border-0 w-100" type="text" name="a7_1_1" value="'''+str(programworktable1.a7_1_1)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" type="text" name="a7_1_2" value="'''+str(programworktable1.a7_1_2)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" type="text" name="a7_1_3" value="'''+str(programworktable1.a7_1_3)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" type="text" name="a7_1_4" value="'''+str(programworktable1.a7_1_4)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" type="text" name="a7_1_5" value="'''+str(programworktable1.a7_1_5)+'''" placeholder=""></td>
                            </tr>

                        </tbody>
                    </table>

                </div>
            </div>
        </div>
        <div class="mb-3 row">
            <label style="text-transform: lowercase;" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-warning">7.2</span> При горизонтальной и высотной съемках застроенных территорий</label>
            <div class="col-sm-9">
                <p>'''+str(form.a7_2)+'''</p>
            </div>
        </div>
        <div class="mb-3 row">
            <label style="text-transform: lowercase;" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-warning">7.3</span> Привязка инженерно-геологических выработок, геофизических и др. точек</label>
            <div class="col-sm-9">
                <p">'''+str(form.a7_3)+'''</p>
            </div>
        </div>
        <div class="mb-3 row">
            <label style="text-transform: lowercase;" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-warning">7.4</span> Составление топографических планов</label>
            <div class="col-sm-9">
                <p>'''+str(form.a7_4)+'''</p>
            </div>
        </div>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary">8</span> СЪЕМКА ПОДЗЕМНЫХ И НАЗЕМНЫХ КОММУНИКАЦИЙ</label>
            <div class="col-sm-9">
                <p>'''+str(form.a8)+'''</p>
            </div>
        </div>
        <div class="mb-3 row">
            <label style="text-transform: lowercase;" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-warning">8.1</span> Составление планов подземных коммуникаций</label>
            <div class="col-sm-9">
                <p>'''+str(form.a8_1)+'''</p>
            </div>
        </div>
        <h5 style="text-align: center" class="text-center"><span class="badge rounded-pill badge-primary">9</span> ИНЖЕНЕРНЫЕ ИЗЫСКАНИЯ ДЛЯ ЛИНЕЙНОГО СТРОИТЕЛЬСТВА</h5>
        <div class="mb-3 row">
            <label style="text-transform: lowercase;" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-warning">9.1</span> Виды, объемы и технические характеристики линейных сооружений, подлежащих изысканиям</label>
            <div class="col-sm-9">
                <p>'''+str(form.a9_1)+'''</p>
            </div>
        </div>
        <h6 class=""><span class="badge rounded-pill badge-warning">9.2</span> Перечень материалов, представляемых по окончании работы</h6>
        <div class="col-sm-12">
            <div class="card border-0">
                <div class="table-responsive">

                    <table class="table table-bordered" id="childTable4">
                        <thead class="bg-primary">
                            <tr>
                                <th scope="col">Наименование трассы, участка</th>
                                <th scope="col">Масштаб плана трассы</th>
                                <th scope="col">Масштаб продольного профиля</th>
                                <th scope="col">Масштаб продольного профиля горизонтальный</th>
                                <th scope="col">Масштаб продольного профиля вертикальный</th>
                                <th scope="col">Масштаб перехода горизонтальный</th>
                                <th scope="col">Масштаб перехода вертикальный</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><input class="border-0 w-100" name="a9_2_1" value="'''+str(programworktable2.a9_2_1)+'''" type="text" placeholder=""></td>
                                <td><input class="border-0 w-100" name="a9_2_2" type="text" value="'''+str(programworktable2.a9_2_2)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" name="a9_2_3" type="text" value="'''+str(programworktable2.a9_2_3)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" name="a9_2_4" type="text" value="'''+str(programworktable2.a9_2_4)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" name="a9_2_5" type="text" value="'''+str(programworktable2.a9_2_5)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" name="a9_2_6" type="text" value="'''+str(programworktable2.a9_2_6)+'''" placeholder=""></td>
                                <td><input class="border-0 w-100" name="a9_2_7" type="text" value="'''+str(programworktable2.a9_2_7)+'''" placeholder=""></td>
                               
                            </tr>

                        </tbody>
                    </table>

                </div>
            </div>
        </div>
        <div class="mb-3 row">
            <label style="text-transform: lowercase;" class="col-sm-3 col-form-label">Ведомости:</label>
            <div class="col-sm-9">
                <input class="form-control" name="a9_3" type="text" value="'''+str(form.a9_3)+'''" placeholder="наименование">
            </div>
        </div>
        <div class="mb-3 row">
            <label style="text-transform: lowercase;" class="col-sm-3 col-form-label">Прочие материалы:</label>
            <div class="col-sm-9">
                <input class="form-control" name="a9_4" type="text" value="'''+str(form.a9_4)+'''" placeholder="наименование">
            </div>
        </div>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary">10</span> ТЕХНИЧЕСКИЙ КОНТРОЛЬ И ПРИЕМКА РАБОТ</p>
            <div class="col-sm-9">
                <p>'''+str(form.a10)+'''</p>
            </div>
        </div>
        <h5 style="text-align: center" class="text-center"><span class="badge rounded-pill badge-primary">11</span> ТЕХНИКА БЕЗОПАСНОСТИ</h5>
        <p>
            К работе допускаются лица, прошедшие вводный инструктаж по технике безопасности, соблюдению полевой гигиены и санитарии
            <p>'''+str(form.a11)+'''</p>
        </p>
        <div class="mb-3 row">
            <p style="text-align: center" class="col-sm-3 col-form-label"><span class="badge rounded-pill badge-primary">12</span> ИСПОЛНИТЕЛИ И СРОКИ ВЫПОЛНЕНИЯ РАБОТ</p>
            <div class="col-sm-9">
                <p>'''+str(form.a12)+'''</p>
            </div>
        </div>
        <h5 style="text-align: center"><span class="badge rounded-pill badge-primary">13</span> ПЕРЕЧЕНЬ МАТЕРИАЛОВ, ПРИЛАГАЕМЫХ К ПРОГРАММЕ</h5>

        <div class="floder_input">
            <div class="row">''';

        if programworkfile.file1:
            context +='''<a href="http://0.0.0.0:1515/'''+str(programworkfile.file1)+'''"><i class="fa fa-file-pdf-o"></i>Копии задания на производство изысканий </a><br>''';
        else:
            context +='';
        if programworkfile.file2:
            context +='''<a href="http://0.0.0.0:1515/'''+str(programworkfile.file2)+'''"><i class="fa fa-file-pdf-o"></i>Схема топографо-геодезической изученности района (участка) работ </a><br>''';
        else:
            context +='';
        if programworkfile.file3:
            context += '''<a href="http://0.0.0.0:1515/'''+str(programworkfile.file3)+'''"><i class="fa fa-file-pdf-o"></i>Схема проектируемой опорной геодезической сети </a><br>''';
        else:
            context +='';
        if programworkfile.file4:
            context += '''<a href="http://0.0.0.0:1515/'''+str(programworkfile.file4)+'''"><i class="fa fa-file-pdf-o"></i>Картограмма расположения участков топографической съемки </a><br>''';
        else:
            context += '';
        if programworkfile.file5:
            context +='''<a href="http://0.0.0.0:1515/'''+str(programworkfile.file5)+'''"><i class="fa fa-file-pdf-o"></i>Чертежи специальных геодезических центров, если намечена их закладка </a><br>''';
        else:
            context +='';
        if programworkfile.file6:
            context += '''<a href="http://0.0.0.0:1515/'''+str(programworkfile.file6)+'''"><i class="fa fa-file-pdf-o"></i>Топографические карты (планы) с указанием проектных вариантов трасс </a><br>''';
        else:
            context +='';
        if programworkfile.file7:
            context += '''<a href="http://0.0.0.0:1515/'''+str(programworkfile.file7)+'''"><i class="fa fa-file-pdf-o"></i>Схема линейных сооружений </a><br>''';
        else:
            context +='';
        context+='''<h5 class="m-t-15">Примечание. <i>Допускается совмещение прилагаемых схем и картограмм.</i></h5>
            </div>
        </div>

        <div class="m-b-20 m-t-20 row">
            <label class="col-sm-3 col-form-label">Программу составил</label>
            <div class="col-sm-9">
                <input class="form-control" name="program_work_creator" type="text" value="'''+str(form.program_work_creator)+'''">
            </div>
        </div>


    </div>

</body>

</html>
               ''';

        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
            'orientation': 'portrait',
            # landscape bu albomiy qiladi
        }
        # display = Display(visible=0, size=(500, 500)).start()
        pdfkit.from_string(context, 'topografiya/static/files/program-work/program_work_file.pdf', options)

        response = HttpResponse(data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="program_work_file.pdf"'
        return response
    else:
        return HttpResponse(0)


def doing_akt_komeral_file(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('data-id')
        work = AktKomeralForm.objects.filter(object=id).first()

        context = '''
        <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        li {
            padding: 5px;
        }
        th,tr,table,td{
            border: 1px solid black
        }
        input{
                border: 0px solid;
        }
        textarea{
            border: 0px solid;
        }
        body{
            font-size: 20px;
        }
          p {
        margin: 0;
        color: #111727 !important;
    }


    </style>
</head>

<body>

    <div style="padding: 100px">

         <div class="col-md-12">
                                                <p style="float: right">ШНК 1.02.07-19 стр.</p>
             <br>
                                                <div class="row" style="float: right">
                                                    <div class="col-xl-8"></div>
                                                    <div class="col-xl-4 col-sm-5 col-lg-5">
                                                        <div class="text-end input-group date" id="dt-minimum"
                                                             data-target-input="nearest">
                                                            <p>'''+str(work.a1)+'''</p>
                                                            <div class="input-group-text" data-target="#dt-minimum"
                                                                 data-toggle="datetimepicker"><i
                                                                    class="fa fa-calendar"> </i></div>
                                                        </div>
                                                    </div>
                                                </div>

                                                <br>
                                                <h3 style="text-align: center">А К Т</h3>
                                                <h4 class="mb-3 " style="text-align: center">Камеральной проверки и приемки
                                                    топографических работ <span></span>
                                                    <br>
                                                </h4>
                                                <form class="theme-form">
                                                    <div class="mb-3 row">
                                                        По объекту: <p>'''+str(work.a2)+'''</p>
                                                        <br>
                                                    </div>
                                                    <div class="mb-3 row">
                                                        Проверка и приемка
                                                            произведена
                                                            <p>'''+str(work.a3)+'''</p>
                                                            <br>
                                                    </div>
                                                    <div class="mb-3 row">
                                                       В присутствии
                                                        исполнителя
                                                        
                                                            <p>'''+str(work.a4)+'''</p>
                                                            <br>
                                                    </div>
                                                    <div class="mb-3 row">
                                                        В процессе проверки
                                                            установлено:
                                                            <br>
                                                            1. Топографические работы выполнены в соответствии '''+str(work.a5)+'''
                                                        <br>
                                                    </div>
                                                    <div class="mb-3 row">
                                                         2.Работа
                                                            выполнена в границах
                                                            '''+str(work.a6)+''' 
                                                            и в следующих объемах:
                                                        <br>
                                                    </div>
                                                    <br>
                                                </form>
                                                <div class="col-sm-12">
                                                    <div class="card border-0">
                                                        <div class="table-responsive">
                                                            <table class="table table-bordered">
                                                                <thead class="bg-primary">
                                                                <tr>
                                                                    <th scope="col">№</th>
                                                                    <th scope="col">Наименование виды работ</th>
                                                                    <th scope="col">Ед.измерения</th>
                                                                    <th scope="col">Объем работ <br>по заданию</th>
                                                                    <th scope="col">Объем работ <br> факти-ческий</th>
                                                                    <th scope="col">Категория работ</th>
                                                                </tr>
                                                                </thead>
                                                                <tbody>
                                                                <tr>
                                                                    <th class="bg-primary" scope="row">1</th>
                                                                    <td>Отыскивание исходных пунктов</td>
                                                                    <td>знак</td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a7" value="'''+str(work.a7)+'''" name="a7"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a8" name="a8" value="'''+str(work.a8)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a9" name="a9" value="'''+str(work.a9)+'''"></td>
                                                                </tr>
                                                                <tr>
                                                                    <th class="bg-primary" scope="row">2</th>
                                                                    <td>Создание обоснования</td>
                                                                    <td>км</td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a10" name="a10" value="'''+str(work.a10)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a11" name="a11" value="'''+str(work.a11)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a12" name="a12" value="'''+str(work.a12)+'''"></td>
                                                                </tr>
                                                                <tr>
                                                                    <th class="bg-primary" scope="row">3</th>
                                                                    <td>Техническое нивелирование</td>
                                                                    <td>км</td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a13" name="a13" value="'''+str(work.a13)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a14" name="a14" value="'''+str(work.a14)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a15" name="a15" value="'''+str(work.a15)+'''"></td>
                                                                </tr>
                                                                <tr>
                                                                    <th class="bg-primary" scope="row">4</th>
                                                                    <td>Закладка центров</td>
                                                                    <td>знак</td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a16" name="a16" value="'''+str(work.a16)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a17" name="a17" value="'''+str(work.a17)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a18" name="a18" value="'''+str(work.a18)+'''"></td>
                                                                </tr>
                                                                <tr>
                                                                    <th class="bg-primary" scope="row">5</th>
                                                                    <td>Координирование углов</td>
                                                                    <td>точка</td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a19" name="a19" value="'''+str(work.a19)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a20" name="a20" value="'''+str(work.a20)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a21" name="a21" value="'''+str(work.a21)+'''"></td>
                                                                </tr>
                                                                <tr>
                                                                    <th class="bg-primary" scope="row">6</th>
                                                                    <td>
                                                                        Тахеометрическая съемка М 1:
                                                                        <span><input
                                                                                style="border: none;border-bottom: 1px solid #cccccc"
                                                                                type="text" id="a22" name="a22" value="'''+str(work.a22)+'''"></span>
                                                                        сечением рельефа горизонталями через
                                                                        <span><input
                                                                                style="border: none;border-bottom: 1px solid #cccccc"
                                                                                type="text" id="a23" name="a23" value="'''+str(work.a23)+'''"></span>м
                                                                    </td>
                                                                    <td>га</td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a24" name="a24" value="'''+str(work.a24)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a25" name="a25" value="'''+str(work.a25)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a26" name="a26" value="'''+str(work.a26)+'''"></td>
                                                                </tr>
                                                                <tr>
                                                                    <th class="bg-primary" scope="row">7</th>
                                                                    <td>
                                                                        Корректура съемки М 1:
                                                                        <span><input
                                                                                style="border: none;border-bottom: 1px solid #cccccc"
                                                                                type="text" id="a27" name="a27" value="'''+str(work.a27)+'''"></span>
                                                                    </td>
                                                                    <td>га</td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a28" name="a28" value="'''+str(work.a28)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a29" name="a29" value="'''+str(work.a29)+'''"></td>
                                                                    <td><input class="border-0 w-100" type="text"
                                                                               placeholder="" id="a30" name="a30" value="'''+str(work.a30)+'''"></td>
                                                                </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                </div>
                                                <br>
                                                <p><span class="badge rounded-pill badge-primary">3.</span> Работы
                                                    выполнены в <span><input style="border:1px solid #e6edef;"
                                                                             type="text" id="a31" name="a31" value="'''+str(work.a31)+'''"></span> системе
                                                    координат и в <input style="border:1px solid #e6edef;"
                                                                             type="text" id="a32" name="a32" value="'''+str(work.a32)+'''"> системе высот.</p>
                                                <br>
                                                <p>Результаты полевого контроля:</p>
                                                <p><span class="badge rounded-pill badge-primary">4.</span> Исходными
                                                    пунктами для построения съемочного обоснования послужили:</p>
                                                '''+str(work.a33)+'''
                                                <br>
                                                <p class="m-t-10">и грунтовые репера <span>
                                                    <input
                                                        style="border:1px solid #e6edef;width: 39%" type="text" id="a34" name="a34" value="'''+str(work.a34)+'''"></span>
                                                    имеющие отметки нивелирования <span><input
                                                            style="border:1px solid #e6edef;" type="text" id="a35" name="a35" value="'''+str(work.a35)+'''"></span> кл.
                                                </p>
                                                <br>
                                                <p>
                                                    <span class="badge rounded-pill badge-primary">5.</span>
                                                    Длины ходов от
                                                    <span><input style="border:1px solid #e6edef;" type="text" id="a36" name="a36" value="'''+str(work.a36)+'''"></span>
                                                    до
                                                    <span><input style="border:1px solid #e6edef;" type="text" id="a37" name="a37" value="'''+str(work.a37)+'''"></span>
                                                    км Абсолютные ошибки от
                                                    <span><input style="border:1px solid #e6edef;" type="text" id="a38" name="a38" value="'''+str(work.a38)+'''"></span>
                                                    до
                                                    <span><input class="m-b-10" style="border:1px solid #e6edef;"
                                                                 type="text" id="a39" name="a39" value="'''+str(work.a39)+'''"></span>
                                                    м.Относительные ошибки от
                                                    <span><input style="border:1px solid #e6edef;" type="text" id="a40" name="a40" value="'''+str(work.a40)+'''"></span>
                                                    до
                                                    <span><input style="border:1px solid #e6edef;" type="text" id="a41" name="a41" value="'''+str( work.a41)+'''"></span>.
                                                    Система ходов уравнена
                                                    <span><input style="border:1px solid #e6edef;" type="text" id="a42" name="a42" value="'''+str(work.a42)+'''"></span>.
                                                </p>
                                                <br>
                                                <form class="theme-form">
                                                    <div class="mb-3 row">
                                                        <span class="badge rounded-pill badge-primary">6.</span>
                                                            Техническое нивелирование выполнено '''+str(work.a43)+'''
                                                    </div>
                                                     <br>
                                                    <p><span class="badge rounded-pill badge-primary">7.</span> Состояние
                                                        полевой документации:</p>
                                                    <div class="mb-3 row">
                                                        <br>
                                                        журналы: '''+str(work.a44)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                        <br>
                                                        схемы: '''+str(work.a45)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                        <br>
                                                        абрисы: '''+str(work.a46)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                        Акт сдачи пунктов на наблюдение за сохранностью '''+str(work.a47)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                        Каталог: '''+str(work.a48)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                        Вычислительные материалы '''+str(work.a49)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                        Пояснительная записка,
                                                            тех. отчет '''+str(work.a50)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                        <br>
                                                        <span class="badge rounded-pill badge-primary">8</span> 
                                                                Замечания по оформлению планшетов
                                                       
                                                            '''+str(work.a51)+'''
                                      
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                        Замечания исправил '''+str(work.a52)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                        <br>
                                                        Заключение по работе в целом и оценка качества работ '''+str(work.a53)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                        <br>
                                                        Работу сдал:  '''+str(work.a54)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                        Работу принял:  '''+str(work.a55)+'''
                                                    <br>
                                                    </div>
                                                    <h5 class="text-center m-b-20 m-t-20"><span
                                                            class="badge rounded-pill badge-primary">9</span>
                                                        камерального контроля и приемки работ по съемке инженерных
                                                        сетей.
                                                    </h5>
                                                    <br>
                                                    <h4 style="text-align: center">Результаты камерального контроля ИПК:</h4>
                                                    <br>
                                                    <p>
                                                        Топографическая съемка инженерных сетей проверена на '''+str(work.a56)+''' листах(е), и/или планшетах(е) с номенклатурой:
                                                        '''+str(work.a57)+'''
                                                    </p>
                                                    <div class="mb-3 row">
                                                        Замечание по экспликации колодцев и опор '''+str(work.a58)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                        <br>
                                                        Замечания исправил '''+str(work.a59)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                        <br>
                                                        Заключение '''+str(work.a60)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                        Оценка качества работ : '''+str(work.a61)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                        Работу сдал: '''+str(work.a62)+'''
                                                    </div>
                                                    <div class="mb-3 row">
                                                    <br>
                                                       Работу принял : '''+str(work.a63)+'''
                                                    </div>
                                                </form>
                                            </div>

    </div>

</body>

</html>
               ''';

        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
            'orientation': 'portrait',
            # landscape bu albomiy qiladi
        }
        # display = Display(visible=0, size=(500, 500)).start()
        pdfkit.from_string(context, 'topografiya/static/files/akt-komeral/akt_komeral.pdf', options)

        response = HttpResponse(data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="akt_komeral.pdf"'
        return response
    else:
        return HttpResponse(0)

def doing_poyasitelniy_file(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('object-id')
        object=WorkerObject.objects.filter(object=id).first()
        print(object)
        form = PoyasitelniyForm.objects.filter(workerobject=object.id).first()
        print(form)
        form1 = PoyasitelniyFormTable1.objects.filter(poyasitelniyform=form).first()
        form2 = PoyasitelniyFormTable2.objects.filter(poyasitelniyform=form).first()
        form3 = PoyasitelniyFormTable3.objects.filter(poyasitelniyform=form).first()
        form4 = PoyasitelniyFormTable4.objects.filter(poyasitelniyform=form).first()

        context = '''
        <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        li {
            padding: 5px;
        }
        th,tr,table,td{
            border: 1px solid black
        }
        input{
                border: 0px solid;
                display: inline-block;
        }

        textarea{
            border: 0px;
        }

        body{
            font-size: 20px;
        }
          p {
        margin: 0;
        color: #111727 !important;
    }

    </style>
</head>

<body>

    <div style="padding: 100px">
         <div class="card">
                            <div class="card-body">
                                <form action="#" method="POST">
                                    <div class="setup-content" id="step-1">
                                        <div class="col-xs-12">
                                            <div class="file-sidebar ">
                                                <div class="pricing-plan border-0">
                                                    <div class="col-md-12">
                                                        <h2 style="text-align: center">ПОЯСНИТЕЛЬНАЯ ЗАПИСКА</h2>
                                                        <p style="text-align: center">по топографо-геодезическим работам</p>
                                                        <br>
                                                        <div class="row">
                                                            <div class="mb-3 row">
                                                                1. Топографо-геодезические работы  '''+str(form.b1)+'''
                                                                <br><br>
                                                            </div>
                                                            <div class="mb-3 row m-t-15">
                                                                2. Топографо-геодезические работы выполнялись в соответствии с техническим заданием, выданным '''+str(form.b2)+'''
                                                                <br>
                                                                <br>
                                                            </div>
                                                            <p>
                                                                и договором № '''+str(form.b_1)+''' от "'''+str(form.b_2)+'''" г
                                                                <br><br>
                                                            </p>
                                                            <div class="mb-3 row m-t-15">
                                                                3. Полевые топографо-геодезические работы выполнены в соответствии с действующими градостроительными нормами бригадой в составе '''+str(form.b3)+'''
                                                                <br>
                                                                <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                               3.1 Ответственный исполнитель '''+str(form.b3_1)+'''
                                                                <br>
                                                                <br>
                                                            <div class="mb-3 row">
                                                                4. Начальник партии '''+str(form.b4)+'''
                                                                    <br>
                                                                    <br>

                                                            </div>
                                                            <div class="mb-3 row">
                                                                5. Система координат '''+str(form.b5)+'''
                                                                <br>
                                                                <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                                6. Система высот '''+str(form.b6)+'''
                                                                    <br>
                                                                <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                                7. Исходные пункты (плановые и высотные) '''+str(form.b7)+'''
                                                                <br>
                                                                <br>
                                                            </div>
                                                            <h5 class="text-center"><span class="badge rounded-pill badge-primary">8</span> Виды и объемы выполненных топографо-геодезических работ приводятся в табл. 1</h5>
                                                            <p class="text-end">Таблица 1</p>
                                                            <div class="col-sm-12 m-t-10">
                                                                <div class="card border-0">
                                                                    <div class="table-responsive">
                                                                        <table class="table table-bordered" id="childTable8">

                                                                            <thead class="table-primary">
                                                                            <tr>
                                                                                <th scope="col">№</th>
                                                                                <th scope="col">Наименование работ</th>
                                                                                <th scope="col">Измеритель</th>
                                                                                <th scope="col">Объемы работ по проекту</th>
                                                                                <th scope="col">Фактически выполнено</th>

                                                                            </tr>
                                                                            </thead>

                                                                            <tbody>
                                                                            <tr>
                                                                                <td scope="row">1</td>
                                                                                <td>
                                                                                   '''+str(form1.b8_1)+'''
                                                                                </td>
                                                                                <td>
                                                                                    '''+str(form1.b8_2)+'''
                                                                                </td>
                                                                                <td>
                                                                                    '''+str(form1.b8_3)+'''
                                                                                </td>
                                                                                <td>
                                                                                   '''+str(form1.b8_4)+'''
                                                                                </td>
                                                                            </tr>
                                                                            </tbody>

                                                                        </table>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <br>

                                                            <div class="mb-3 row">
                                                                8.1 Номенклатура планшетов '''+str(form.b8_1_1)+'''
                                                                <br>
                                                            </div>
                                                            <h5 class="text-center"><span class="badge rounded-pill badge-primary">9</span> Каталог координат и высот исходных пунктов и точек долговременного закрепления</h5>
                                                            <div class="col-sm-12 m-t-10">
                                                                <div class="card border-0">
                                                                    <div class="table-responsive">
                                                                        <table class="table table-bordered" id="childTable9">
                                                                            <thead class="table-primary">
                                                                            <tr>
                                                                                <th scope="col">№</th>
                                                                                <th scope="col">Номер пункта и тип закрепления</th>
                                                                                <th scope="col">Координаты x</th>
                                                                                <th scope="col">Координаты y</th>
                                                                                <th scope="col">Высота</th>

                                                                            </tr>
                                                                            </thead>
                                                                            <tbody>
                                                                            <tr>
                                                                                <td scope="row">1</td>
                                                                                <td>
                                                                                    '''+str(form2.b9_1)+'''
                                                                                </td>
                                                                                <td>
                                                                                     '''+str(form2.b9_2)+'''
                                                                                </td>
                                                                                <td>
                                                                                     '''+str(form2.b9_3)+'''
                                                                                </td>

                                                                                <td>
                                                                                    '''+str(form2.b9_4)+'''
                                                                                </td>
                                                                            </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <br>
                                                                <br>
                                                            <div class="mb-3 row">
                                                                10. Планово-высотное обоснование выполнено '''+str(form.b10)+'''
                                                                        <br>
                                                                <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                                11. Пункты съемочного обоснования закреплены '''+str(form.b11)+'''
                                                                <br>
                                                                <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                               12. Постоянные геодезические знаки сданы по акту на наблюдение за сохранностью представителю '''+str(form.b12)+'''
                                                                           <br>
                                                                <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                                    13. Угловые измерения проводились '''+str(form.b13)+'''
                                                                    <br>
                                                                <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                                14. Линейные измерения выполнены '''+str(form.b14)+'''
                                                                <br>
                                                                <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                               15. Нивелирование производилось нивелиром '''+str(form.b15)+'''
                                                                <br>
                                                            </div>
                                                            <h5><span class="badge rounded-pill badge-primary">16</span> Уравнивание съёмочного обоснования произведено:</h5>
                                                            <div class="mb-3 row">
                                                                    a) планового '''+str(form.b16_a)+'''
                                                                    <br>
                                                                    <br>
                                                            </div>
                                                            <div class="mb-3 row">
                                                                б) высотного '''+str(form.b16_b)+'''
                                                                <br>
                                                                <br>
                                                            </div>
                                                        </div>
                                                    </div>

                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="setup-content" id="step-2">
                                        <div class="col-xs-12">
                                            <h5 class="text-center"><span class="badge rounded-pill badge-primary">17</span> Техническая характеристика планового съемочного обоснования приводится в таблице 2.</h5>
                                            <p class="text-end"> Таблица 2</p>
                                            <div class="col-sm-12 m-t-10">
                                                <div class="card border-0">
                                                    <div class="table-responsive">
                                                        <table class="table table-bordered" id="childTableTen">
                                                            <thead class="table-primary">
                                                            <tr>
                                                                <th scope="col">№</th>
                                                                <th scope="col">Наименование хода</th>
                                                                <th scope="col">Длина хода в км</th>
                                                                <th scope="col">Число узлов</th>
                                                                <th scope="col">Угловые невязки получен</th>
                                                                <th scope="col">Угловые невязки допустим</th>
                                                                <th scope="col">Линейные невязки абсолют</th>
                                                                <th scope="col">Линейные невязки относит</th>

                                                            </tr>
                                                            </thead>
                                                            <tbody>
                                                            <tr>
                                                                <td scope="row">1</td>
                                                                <td>
                                                                     '''+str(form3.b17_1)+'''
                                                                </td>
                                                                <td>

                                                                   '''+str(form3.b17_2)+'''
                                                                </td>
                                                                <td>
                                                                    '''+str(form3.b17_3)+'''
                                                                </td>
                                                                <td>
                                                                    '''+str(form3.b17_4)+'''
                                                                </td>
                                                                <td>
                                                                    '''+str(form3.b17_5)+'''
                                                                </td>
                                                                <td>
                                                                    '''+str(form3.b17_6)+'''
                                                                </td>
                                                                <td>
                                                                    '''+str(form3.b17_7)+'''
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            </div>
                                            <h5 class="text-center"><span class="badge rounded-pill badge-primary">18</span> Техническая характеристика высотного съемочного обоснования приводится в таблице 3.</h5>
                                            <div class="col-sm-12 m-t-10">
                                                <div class="card border-0">
                                                    <div class="table-responsive">
                                                        <table class="table table-bordered" id="childTableEleven">
                                                            <thead class="table-primary">
                                                            <tr>
                                                                <th scope="col">№</th>
                                                                <th scope='col'>Наименование хода</th>
                                                                <th scope="col">Число станций км/хода</th>
                                                                <th scope="col">Невязки в ходах в мм получен</th>
                                                                <th scope="col">Невязки в ходах в мм допустим</th>
                                                                <th scope="col">Примечание</th>

                                                            </tr>
                                                            </thead>
                                                            <tbody>
                                                            <tr>
                                                                <td scope="row">1</td>
                                                                <td>
                                                                   '''+str(form4.b18_1)+'''
                                                                </td>
                                                                <td>
                                                                    '''+str(form4.b18_2)+'''
                                                                </td>
                                                                <td>
                                                                        '''+str(form4.b18_3)+'''
                                                                </td>
                                                                <td>
                                                                    '''+str(form4.b18_4)+'''
                                                                </td>
                                                                <td>'''+str(form4.b18_5)+'''</td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="mb-3 row">
                                                19. Топографическая съемка '''+str(form.b19)+'''
                                                 <br>
                                                <br>
                                            </div>
                                            <div class="mb-3 row">
                                                19.1 Горизонтальная съемка застроенной территории производилась '''+str(form.b19_1)+'''
                                                <br>
                                                <br>
                                            </div>
                                            <div class="mb-3 row">
                                                19.2 Высотная съемка застроенной территории производилась '''+str(form.b19_2)+'''
                                                 <br>
                                                <br>
                                            </div>
                                            <div class="mb-3 row">
                                                20. Обновление топографической съемки '''+str(form.b20)+'''
                                                 <br>
                                                <br>
                                            </div>
                                            <h5 class="">21. По выявлению и съёмке подземных коммуникаций на объекте:</h5>
                                            <div class="mb-3 row">
                                                Работа выполнена исполнителем '''+str(object.object.worker_ispolnitel)+'''
                                                <br>
                                                <br>
                                            <p>в нижеследующем объёме:</p>
                                            <div class="col-sm-12">
                                                <div class="card border-0">
                                                    <div class="table-responsive">
                                                        <table class="table table-bordered">
                                                            <thead class="table-primary">
                                                            <tr>
                                                                <th scope="col">№</th>
                                                                <th scope="col">Виды работ</th>
                                                                <th scope="col">Ед.измерен</th>
                                                                <th scope="col">Объём работ</th>
                                                                <th scope="col">Категория</th>
                                                            </tr>
                                                            </thead>
                                                            <tbody>
                                                            <tr>
                                                                <th scope="row">1</th>
                                                                <td>Рекогносцировка трасс ИПК</td>
                                                                <td>км</td>
                                                                <td>'''+str(form.c_1)+'''</td>
                                                                <td>'''+str(form.c_2)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">2</th>
                                                                <td>Прослушивание и привязка точек ИПК</td>
                                                                <td>точка</td>
                                                                <td>'''+str(form.c_3)+'''</td>
                                                                <td>'''+str(form.c_4)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">3</th>
                                                                <td>Прослушивание точек ИПК без привязки с К=0,56</td>
                                                                <td>точка</td>
                                                                <td>'''+str(form.c_5)+'''</td>
                                                                <td>'''+str(form.c_6)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">4</th>
                                                                <td>Определение глубин заложения ИПК</td>
                                                                <td>точка</td>
                                                                <td>'''+str(form.c_7)+'''</td>
                                                                <td>'''+str(form.c_8)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">5</th>
                                                                <td>Привязка выходов ИПК</td>
                                                                <td>точка</td>
                                                                <td>'''+str(form.c_9)+'''</td>
                                                                <td>'''+str(form.c_10)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">6</th>
                                                                <td>Обследование колодцев</td>
                                                                <td>колодец</td>
                                                                <td>'''+str(form.c_11)+'''</td>
                                                                <td>'''+str(form.c_12)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">7</th>
                                                                <td>Нивелирование колодцев с коэффициентом = 0,5</td>
                                                                <td>га</td>
                                                                <td>'''+str(form.c_13)+'''</td>
                                                                <td>'''+str(form.c_14)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">8</th>
                                                                <td>Описание надземных сооружений, коммуникаций</td>
                                                                <td>опора,узел</td>
                                                                <td>'''+str(form.c_15)+'''</td>
                                                                <td>'''+str(form.c_16)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">9</th>
                                                                <td>Нивелирование надземных сооружений</td>
                                                                <td>опора, точка</td>
                                                                <td>'''+str(form.c_17)+'''</td>
                                                                <td>'''+str(form.c_18)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">10</th>
                                                                <td>Обследование территории съёмки, где отсутствуют ИПК</td>
                                                                <td>га</td>
                                                                <td>'''+str(form.c_19)+'''</td>
                                                                <td>'''+str(form.c_20)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">11</th>
                                                                <td>Обследование колодцев с К=0,5; (завален, залит)</td>
                                                                <td>колодец</td>
                                                                <td>'''+str(form.c_21)+'''</td>
                                                                <td>'''+str(form.c_22)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">12</th>
                                                                <td>Составление ведомости экспликации колодцев ИПК</td>
                                                                <td>колодец</td>
                                                                <td>'''+str(form.c_23)+'''</td>
                                                                <td>'''+str(form.c_24)+'''</td>
                                                            </tr>
                                                            <tr>
                                                                <th scope="row">13</th>
                                                                <td>Составление планов ИПК</td>
                                                                <td>га</td>
                                                                <td>'''+str(form.c_25)+'''</td>
                                                                <td>'''+str(form.c_26)+'''</td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        </div>
                                    </div>

                                    <div class="setup-content" id="step-3">
                                        <div class="col-xs-12">
                                            <h5>Инженерные подземные сети представлены:</h5>
                                            <div class="mb-3 row">
                                                1. Работа выполнена исполнителем '''+str(form.d_1)+'''
                                                <br><br>
                                            </div>
                                            <div class="mb-3 row">
                                                2. Самотечные трубопроводы: '''+str(form.d_2)+'''
                                                    <br><br>
                                            </div>
                                            <div class="mb-3 row">
                                                3. Кабельныелинии: '''+str(form.d_3)+'''
                                                <br>
                                                <br>
                                            </div>
                                            <p>
                                                Неметаллические трубопроводы и резервные кабели '''+str(form.d_4)+'''  на планшета '''+str(form.d_5)+''' нанесены по неуточнённым данным '''+str(form.d_6)+'''
                                                <br>
                                                <br>
                                            </p>
                                            <div class="mb-3 row">
                                                Обследование и нивелирование колодцев производилось с использование '''+str(form.d_7)+'''
                                                <br>
                                                <br>
                                            </div>
                                            <div class="mb-3 row">
                                                Прослушивание ИПК выполнялось с применение трубокабелеискателей '''+str(form.d_8)+'''
                                                    <br>
                                                    <br>
                                            </div>
                                            <div class="mb-3 row">
                                                    Привязка точек прослушивания и съёмка выходов ИПК производилась '''+str(form.d_9)+'''
                                                    <br>
                                                    <br>
                                            </div>
                                            <p>
                                                Все выявленные подземные коммуникации нанесены на топографический план в масштабе 1: '''+str(form.d_10)+''' и принятых условных знаках.
                                                <br>
                                                <br>
                                            </p>
                                            <div class="mb-3 row">
                                                Выполненные работы по выявлению подземных коммуникаций проконтролированы и приняты  '''+str(form.d_11)+'''
                                                <br>
                                                <br>
                                            </div>
                                            <div class="mb-3 row">
                                                Записку составил '''+str(form.d_12)+'''
                                                <br>
                                                <br>
                                            </div>
                                            <div class="mb-3 row">
                                                Контроль и приемка работ '''+str(form.d_13)+'''
                                                <br>
                                                <br>
                                            </div>

                                        </div>
                                    </div>

                                </form>
                            </div>
                        </div>

    </div>

</body>

</html>
                ''';

        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
            'orientation': 'portrait',
            # landscape bu albomiy qiladi
        }
        # display = Display(visible=0, size=(500, 500)).start()
        pdfkit.from_string(context, 'topografiya/static/files/poyasitelniy/poyasitelniy.pdf', options)

        response = HttpResponse(data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="poyasitelniy.pdf"'
        return response
    else:
        return HttpResponse(0)

def doing_akt_polevoy_file(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('object-id')
        object = Object.objects.filter(id=id).first()

        workerobject = WorkerObject.objects.filter(object=id).first()
        pdowork = Object.objects.filter(id=id).first()
        siriefiles = SirieFiles.objects.filter(workerobject=workerobject).first()
        order = Order.objects.filter(object=id).first()

        work = AktPolevoyForm.objects.filter(object=id).first()
        work_table1 = AktPolovoyTable1.objects.filter(aktpolovoy=work).first()
        work_table2 = AktPolovoyTable2.objects.filter(aktpolovoy=work).first()
        work_table3 = AktPolovoyTable3.objects.filter(aktpolovoy=work).first()
        work_table4 = AktPolovoyTable4.objects.filter(aktpolovoy=work).first()
        work_table5 = AktPolovoyTable5.objects.filter(aktpolovoy=work).first()
        work_table6 = AktPolovoyTable6.objects.filter(aktpolovoy=work).first()
        work_table7 = AktPolovoyTable7.objects.filter(aktpolovoy=work).first()
        work_table8 = AktPolovoyTable8.objects.filter(aktpolovoy=work).first()


        context = '''
               <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        li {
            padding: 5px;
        }
        th,tr,table,td{
            border: 1px solid black
        }
        input{
                border: 0px solid;
                display: inline-block;
        }

        textarea{
            border: 0px;
        }

        body{
            font-size: 20px;
        }
          p {
        margin: 0;
        color: #111727 !important;
    }

    </style>
</head>

<body>

    <div style="padding: 100px">

<form action="#" method="POST">
                                                                <div class="setup-content" id="step-1">
                                                                    <div class="col-xs-12">
                                                                        <div class="file-sidebar">
                                                                            <div class="pricing-plan">
                                                                                <div class="col-md-12">
                                                                                    <p class="text-end" style="float: right">ШНК
                                                                                        1.02.07-19 </p>
                                                                                    <br>
                                                                                    <p class="text-end" style="float: right">
                                                                                        Приложение F обязательное
                                                                                    </p>
                                                                                    <br>
                                                                                    <div class="row" style="float: right">
                                                                                        <div class="col-lg-8"></div>

                                                                                        <div class="col-xl-4 col-sm-5 col-lg-5">
                                                                                            <div class="text-end input-group date"
                                                                                                 id="dt-minimum"
                                                                                                 data-target-input="nearest">
                                                                                                <input id="a1" name="a1" value="'''+str(work.a1)+'''" class="text-end form-control datetimepicker-input digits"
                                                                                                       type="text"
                                                                                                       data-target="#dt-minimum">
                                                                                                <div class="input-group-text" data-target="#dt-minimum" data-toggle="datetimepicker">
                                                                                                    <i class="fa fa-calendar"> </i>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>

                                                                                    </div>

                                                                                    <h3 class="text-center" style="text-align: center">АКТ</h3>
                                                                                    <div class="col-md-12">
                                                                                        <br>
                                                                                        <h5 class="text-center" style="text-align: center">1. Полевого
                                                                                            контроля и приемки
                                                                                            топографических
                                                                                            работ</h5>
                                                                                        <p>Мы, нижеподписавшиеся: '''+str(work.a2)+'''</p>
                                                                                        <p>составили настоящий акт в
                                                                                            том, что за период с</p>

                                                                                        <div class="input-group date w-50"
                                                                                             id="dt-disab-days"
                                                                                             data-target-input="nearest">
                                                                                            <input class="form-control datetimepicker-input digits"
                                                                                                   type="text" id="a3" value="'''+str(work.a3)+'''" name="a3"
                                                                                                   data-target="#dt-disab-days">

                                                                                            <div class="input-group-text"
                                                                                                 data-target="#dt-disab-days"
                                                                                                 data-toggle="datetimepicker">
                                                                                                <i class="fa fa-calendar"></i>
                                                                                            </div>
                                                                                        </div>

                                                                                        <p>произведен контроль и приемка
                                                                                            топографических работ,
                                                                                            выполненных на объекте:</p>
                                                                                        <input style="width: 50%" id="a4" value="'''+str(work.a4)+'''" name="a4"
                                                                                               class="form-control"
                                                                                               type="text"
                                                                                               placeholder="№ дог.">
                                                                                        <p>по заданию заказчика</p>
                                                                                        <input style="width: 50%" id="a5" value="'''+str(work.a5)+'''" name="a5"
                                                                                               class="form-control"
                                                                                               type="text"
                                                                                               placeholder=""><br>
                                                                                        <h5 class="text-center">виды и
                                                                                            объемы выполненных
                                                                                            работ: </h5>
                                                                                        <div class="col-sm-12">
                                                                                            <div class="card border-0">
                                                                                                <div class="table-responsive">
                                                                                                    <table class="table table-bordered">
                                                                                                        <thead class="bg-primary">
                                                                                                        <tr>
                                                                                                            <th scope="col">
                                                                                                                № п/п
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Наименование
                                                                                                                виды
                                                                                                                работ
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Ед.измерения
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Объем
                                                                                                                работ /
                                                                                                                факт
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Категория
                                                                                                                работ
                                                                                                            </th>
                                                                                                        </tr>
                                                                                                        </thead>
                                                                                                        <tbody>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                1
                                                                                                            </th>
                                                                                                            <td>
                                                                                                                Теодолитные
                                                                                                                хода
                                                                                                            </td>
                                                                                                            <td>км</td>
                                                                                                            <td><input id="a6" name="a6" value="'''+str(work.a6)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a7" name="a7"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work.a7)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                2
                                                                                                            </th>
                                                                                                            <td>
                                                                                                                Техническое
                                                                                                                нивелирование
                                                                                                            </td>
                                                                                                            <td>км</td>
                                                                                                            <td><input id="a8" name="a8" value="'''+str(work.a8)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a9" name="a9" value="'''+str(work.a9)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                3
                                                                                                            </th>
                                                                                                            <td>Закладка
                                                                                                                центров
                                                                                                                тип
                                                                                                            </td>
                                                                                                            <td>знак
                                                                                                            </td>
                                                                                                            <td><input id="a10" name="a10" value="'''+str(work.a10)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a11" name="a11" value="'''+str(work.a11)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                4
                                                                                                            </th>
                                                                                                            <td>
                                                                                                                Координирование
                                                                                                                углов
                                                                                                            </td>
                                                                                                            <td>точ</td>
                                                                                                            <td><input id="a12" name="a12" value="'''+str(work.a12)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a13" name="a13" value="'''+str(work.a13)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                5
                                                                                                            </th>
                                                                                                            <td>
                                                                                                                Мензульная
                                                                                                                съемка
                                                                                                                М1:500
                                                                                                                сеч.м
                                                                                                            </td>
                                                                                                            <td>га</td>
                                                                                                            <td><input id="a14" name="a14" value="'''+str(work.a14)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a15" name="a15" value="'''+str(work.a15)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                6
                                                                                                            </th>
                                                                                                            <td>
                                                                                                                Тахеометрическая
                                                                                                                съемка
                                                                                                                М:1 сеч
                                                                                                                м
                                                                                                            </td>
                                                                                                            <td>га</td>
                                                                                                            <td><input id="a16" name="a16" value="'''+str(work.a16)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a17" name="a17" value="'''+str(work.a17)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                7
                                                                                                            </th>
                                                                                                            <td>
                                                                                                                Корректура
                                                                                                                съемки
                                                                                                                М1:
                                                                                                            </td>
                                                                                                            <td>га</td>
                                                                                                            <td><input id="a18" name="a18" value="'''+str(work.a18)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a19" name="a19" value="'''+str(work.a19)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                8
                                                                                                            </th>
                                                                                                            <td>
                                                                                                                Перенос
                                                                                                                проекта
                                                                                                                в натуру
                                                                                                                и
                                                                                                                исполнительная
                                                                                                                съемка
                                                                                                            </td>
                                                                                                            <td>км</td>
                                                                                                            <td><input id="a20" name="a20" value="'''+str(work.a20)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a21" name="a21" value="'''+str(work.a21)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                        <p>Работы выполнены в
                                                                                            соответствии с программой
                                                                                            работ, в
                                                                                            <span><input id="a22" name="a22" value="'''+str(work.a22)+'''"
                                                                                                    style="border:1px solid #e6edef;"
                                                                                                    type="text"></span>
                                                                                            системе
                                                                                            координат и в
                                                                                            <span><input id="a23" name="a23" value="'''+str(work.a23)+'''"
                                                                                                    style="border:1px solid #e6edef;"
                                                                                                    type="text"></span>
                                                                                            системе высот.</p>
                                                                                        <h6>Результаты полевого
                                                                                            контроля:</h6>
                                                                                        <p>
                                                                                            <span class="badge rounded-pill badge-primary">a)</span>
                                                                                            теодолитные хода
                                                                                        </p>

                                                                                        <div class="col-sm-12 m-t-5">
                                                                                            <div class="card border-0">
                                                                                                <div class="table-responsive">
                                                                                                    <table class="table table-bordered"
                                                                                                           id="childTable">
                                                                                                        <thead class="table-primary">
                                                                                                        <tr>
                                                                                                            <th scope="col">
                                                                                                                №
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Наименование
                                                                                                                хода
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Длина
                                                                                                                хода
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                К-во
                                                                                                                углов
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Угл
                                                                                                                невязки:получ,допуст
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Лин.невязки:абсол,относит
                                                                                                            </th>
                                                                                                            
                                                                                                        </tr>
                                                                                                        </thead>
                                                                                                        <tbody>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                1
                                                                                                            </th>
                                                                                                            <td><input id="a1_1" name="a1_1"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table1.a1_1)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a1_2" name="a1_2"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table1.a1_2)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a1_3" name="a1_3"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table1.a1_3)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a1_4" name="a1_4"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table1.a1_4)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a1_5" name="a1_5"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table1.a1_5)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a1_6" name="a1_6"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table1.a1_6)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a1_7" name="a1_7"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table1.a1_7)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                           
                                                                                                        </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <p>
                                                                                                    выполненные
                                                                                                    <span><input  id="a24" name="a24" value="'''+str(work.a24)+'''"
                                                                                                            class="form-control w-50"
                                                                                                            type="text"></span>
                                                                                                </p>
                                                                                                <p>контрольные</p> '''+str(work.a25)+'''
                                                                                            </div>
                                                                                        </div>
                                                                                        <p><span
                                                                                                class="badge rounded-pill badge-primary">б)</span>
                                                                                            нивелирные хода</p>
                                                                                        <div class="col-sm-12 m-t-5">
                                                                                            <div class="card border-0">
                                                                                                <div class="table-responsive">
                                                                                                    <table class="table table-bordered"
                                                                                                           id="childTable1">
                                                                                                        <thead class="table-primary">
                                                                                                         <tr>
                                                                                                            <th scope="col">
                                                                                                                №
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Наименование
                                                                                                                хода
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Длина
                                                                                                                хода
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                К-во
                                                                                                                штатив
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Невязки в мм
                                                                                                                <br>
                                                                                                                получ
                                                                                                            </th>
                                                                                                             <th scope="col">
                                                                                                                Невязки в мм
                                                                                                                 <br>
                                                                                                                 допуст
                                                                                                            </th>

                                                                                                            <th scope="col">
                                                                                                                Примеч
                                                                                                            </th>
                                                                                                            
                                                                                                        </tr>
                                                                                                        </thead>
                                                                                                        <tbody>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                1
                                                                                                            </th>
                                                                                                            <td><input  id="a2_1" name="a2_1"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder=""value="'''+str(work_table2.a2_1)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a2_2" name="a2_2"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table2.a2_2)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a2_3" name="a2_3"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table2.a2_3)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a2_4" name="a2_4"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table2.a2_4)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a2_5" name="a2_5"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table2.a2_5)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a2_6" name="a2_6"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table2.a2_6)+'''">
                                                                                                            </td>

                                                                                                            
                                                                                                        </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <p>
                                                                                                    выполненные
                                                                                                    <span><input id="a26" name="a26" value="'''+str(work.a26)+'''"
                                                                                                            class="form-control w-50"
                                                                                                            type="text"></span>
                                                                                                </p>
                                                                                                <p>контрольные</p> '''+str(work.a27)+'''
                                                                                            </div>
                                                                                        </div>
                                                                                        <p>Топографическая съемка,
                                                                                            перенос проекта в натуру,
                                                                                            контрольно-испольнительная
                                                                                            съемка (виды выполненных
                                                                                            работ
                                                                                            подчеркнуть)
                                                                                            проверена на
                                                                                            <span><input id="a28" value="'''+str(work.a28)+'''" name="a28" style="border:1px solid #e6edef;" type="text"></span>
                                                                                            планшетах с номенклатурой:
                                                                                            <span>
                                                                                                <input id="a29" value="'''+str(work.a29)+'''" name="a29" style="border:1px solid #e6edef;" type="text"></span>
                                                                                        </p>
                                                                                        <div class="col-sm-12 m-t-10">
                                                                                            <div class="card border-0">
                                                                                                <div class="table-responsive">
                                                                                                    <table class="table table-bordered"
                                                                                                           id="childTable2">
                                                                                                        <thead class="bg-primary">
                                                                                                        <tr>
                                                                                                            <th scope="col">
                                                                                                                №
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Оценка
                                                                                                                качества
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Средняя
                                                                                                                ошибка
                                                                                                                (расхождение)
                                                                                                                в мм
                                                                                                                плана
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Расхождение
                                                                                                                превышающее
                                                                                                                1мм
                                                                                                                плана в
                                                                                                                проц.
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Средняя
                                                                                                                ошибка
                                                                                                                (расхождение)
                                                                                                                в см по
                                                                                                                высоте
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Расхождения
                                                                                                                превышающие
                                                                                                                двойной
                                                                                                                в проц.
                                                                                                            </th>
                                                                                                           
                                                                                                        </tr>
                                                                                                        </thead>
                                                                                                        <tbody>
                                                                                                         <tr>
                                                                                                            <td class="table-primary"
                                                                                                                scope="row">
                                                                                                                1
                                                                                                            </td>
                                                                                                            <td><input id="a3_1" name="a3_1"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_1)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a3_2" name="a3_2"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_2)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a3_3" name="a3_3"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_3)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a3_4" name="a3_4"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_4)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a3_5" name="a3_5"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_5)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a3_6" name="a3_6"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_6)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a3_7" name="a3_7"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_7)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a3_8" name="a3_8"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_8)+'''">
                                                                                                            </td>
                                                                                                            <td>
                                                                                                                <input id="a3_9" name="a3_9"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table3.a3_9)+'''">
                                                                                                            </td>
                                                                                                            
                                                                                                        </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                        <p>Состояние полевой
                                                                                            документации:</p> '''+str(work.a30)+'''
                                                                                        <br>
                                                                                        <p>Замечания по оформлению
                                                                                            планшетов:</p> '''+str(work.a31)+'''

                                                                                    </div>

                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div class="setup-content" id="step-2">
                                                                    <div class="col-xs-12">
                                                                        <div class="file-sidebar">
                                                                            <div class="pricing-plan">
                                                                                <div class="col-md-12">
                                                                                    <p class="text-end">ШНК
                                                                                        1.02.07-19</p>
                                                                                    <h4 class="text-center m-b-40" style="text-align: center">
                                                                                        Таблица контрольных измерений
                                                                                        (план)</h4>
                                                                                    <form action="">

                                                                                        <h6 class="text-center" style="text-align: center">Контроль
                                                                                            и оценка качества
                                                                                            горизонтальной съемки</h6>
                                                                                        <div class="col-sm-12 m-t-5">
                                                                                            <div class="card border-0">
                                                                                                <div class="table-responsive">
                                                                                                    <table class="table table-bordered"
                                                                                                           id="childTable3">
                                                                                                        <thead class="table-primary">
                                                                                                         <tr>
                                                                                                            <th scope="col">
                                                                                                                №
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Расстояния
                                                                                                                с плана
                                                                                                                (м)
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Расстояния
                                                                                                                в натуре (м)
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Расхождения (гр.3-гр.2) (м)
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Расхождения (гр.3-гр.2) d, (мм) плана
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Между
                                                                                                                какими
                                                                                                                контурами
                                                                                                                произведены
                                                                                                                промеры
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Примечание
                                                                                                            </th>
                                                                                                           
                                                                                                        </tr>
                                                                                                        </thead>
                                                                                                        <tbody>
                                                                                                         <tr>
                                                                                                            <th scope="row">
                                                                                                                1
                                                                                                            </th>
                                                                                                            <td><input id="a4_1" name="a4_1"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table4.a4_1)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a4_2" name="a4_2"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="" value="'''+str(work_table4.a4_2)+'''">
                                                                                                            </td>
                                                                                                            <td><input id="a4_3" name="a4_3" value="'''+str(work_table4.a4_3)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a4_4" name="a4_4"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table4.a4_4)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a4_5" name="a4_5"
                                                                                                                    class="border-0 w-100" value="'''+str(work_table4.a4_5)+'''"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a4_6" name="a4_6" value="'''+str(work_table4.a4_6)+'''"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            
                                                                                                        </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                        <p>
                                                                                            Количество расхождений между
                                                                                            ближайшими контурами
                                                                                            (капитальные здания и
                                                                                            сооружения) превышающих
                                                                                            допуск (0,4 мм. плана)
                                                                                            <span><input type="text" id="a32" name="a32" value="'''+str(work.a32)+'''"
                                                                                                         class="form-plan w-50"></span>
                                                                                            Средняя погрешность
                                                                                            положения на плане предметов
                                                                                            и контуров местности с
                                                                                            четкими очертаниями в мм
                                                                                            плана
                                                                                            d<sup>cp</sup>=d/n
                                                                                            <span><input type="text" id="a33" name="a33" value="'''+str(work.a33)+'''"
                                                                                                         class="w-25 m-t-10 form-plan"></span>
                                                                                            мм, при допуске 0,5мм.
                                                                                        </p>
                                                                                        <p>
                                                                                            Количество расхождений,
                                                                                            превышающих удвоенного
                                                                                            значения допустимой средней
                                                                                            ошибки, получено
                                                                                            <span><input type="text" id="a34" name="a34" value="'''+str(work.a34)+'''"
                                                                                                         class="form-plan"></span>,
                                                                                            что составляет
                                                                                            <span><input type="text" id="a35" name="a35" value="'''+str(work.a35)+'''"
                                                                                                         class="form-plan"></span>
                                                                                            %, при допуске 10%.
                                                                                        </p>
                                                                                        <b>Количество расхождений
                                                                                            превышающих предельную
                                                                                            погрешность: </b>
                                                                                        <p>
                                                                                            <span class="badge rounded-pill badge-primary">a)</span>
                                                                                            для капитальной застройки
                                                                                            <span><input type="text" id="a36" name="a36"  value="'''+str(work.a36)+'''"
                                                                                                         class="form-plan"></span>
                                                                                            или % при допуске 5%;
                                                                                            <span class="badge rounded-pill badge-primary">б)</span>
                                                                                            для предметов и контуров
                                                                                            местности с четкими
                                                                                            очертаниями
                                                                                            <span><input type="text" id="a37" name="a37" value="'''+str(work.a37)+'''"
                                                                                                         class="form-plan"></span>
                                                                                            или % при допуске 5%.
                                                                                        </p>
                                                                                        <div class="mb-3 row">
                                                                                            <label class="col-sm-3 col-form-label">Оценка
                                                                                                качества горизонтальной
                                                                                                съемки:</label>
                                                                                            <div class="col-sm-9">
                                                                                                <input class="form-control" id="a38" name="a38" value="'''+str(work.a38)+'''"
                                                                                                       type="text"
                                                                                                       placeholder="">
                                                                                            </div>
                                                                                        </div>
                                                                                        <div class="mb-3 row">
                                                                                            <label class="col-sm-3 col-form-label">Замечания
                                                                                                по пропуску элементов
                                                                                                ситуации, правильности
                                                                                                применения условных
                                                                                                знаков:</label>
                                                                                            <div class="col-sm-9"> '''+str(work.a39)+'''
                                                                                            </div>
                                                                                        </div>


                                                                                        <h4 class="text-center m-b-40 m-t-40" style="text-align: center">
                                                                                            Таблица контрольных
                                                                                            измерений (рельеф)</h4>

                                                                                        <h6 class="text-center" style="text-align: center">Контроль
                                                                                            и оценка качества
                                                                                            горизонтальной съемки</h6>
                                                                                        <div class="col-sm-12 m-t-5">
                                                                                            <div class="card border-0">
                                                                                                <div class="table-responsive">
                                                                                                    <table class="table table-bordered"
                                                                                                           id="childTable4">
                                                                                                        <thead class="table-primary">
                                                                                                        <tr>
                                                                                                            <th scope="col">
                                                                                                                №
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Отметка
                                                                                                                <br>
                                                                                                                с плана
                                                                                                                (м)
                                                                                                            </th>
                                                                                                            <th scope="col">
                                                                                                                Отметка
                                                                                                                <br>
                                                                                                                в натуре (м)
                                                                                                            </th>
                                                                                                            <th scope="col" class="text-center">
                                                                                                                Расхождения (гр.3-гр.2)
                                                                                                                <br> (м)
                                                                                                            </th>
                                                                                                            <th scope="col" class="text-center">
                                                                                                                Расхождения (гр.3-гр.2)
                                                                                                                <br> d, (мм) плана
                                                                                                            </th>
                                                                                                            <th scope="col" class="text-center">
                                                                                                                Наименование
контур
                                                                                                            </th>
                                                                                                            <th scope="col" class="text-center">
                                                                                                                Примечание
                                                                                                            </th>
                                                                                                            
                                                                                                        </tr>
                                                                                                        </thead>
                                                                                                        <tbody>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                1
                                                                                                            </th>
                                                                                                            <td><input id="a5_1" name="a5_1"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table5.a5_1)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a5_2" name="a5_2"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table5.a5_2)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a5_3" name="a5_3"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table5.a5_3)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a5_4" name="a5_4"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table5.a5_4)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a5_5" name="a5_5"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table5.a5_5)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a5_6" name="a5_6"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table5.a5_6)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            
                                                                                                        </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                        <p>
                                                                                            Средняя ошибка в см
                                                                                            H<sub>cp</sub>=H/n=
                                                                                            <span><input type="text" id="a40" name="a40" value="'''+str(work.a40)+'''"
                                                                                                         class="form-plan"></span>
                                                                                            см при допуске
                                                                                            <span><input type="text" id="a41" name="a41" value="'''+str(work.a41)+'''"
                                                                                                         class="form-plan"></span>
                                                                                            см.
                                                                                        </p>
                                                                                        <p>Примечания
                                                                                            Количество предельных
                                                                                            расхождений (не превышающих
                                                                                            удвоенное значение
                                                                                            допустимой средней ошибки)
                                                                                            получено
                                                                                            <span><input type="text" id="a42" name="a42" value="'''+str(work.a42)+'''"
                                                                                                         class="form-plan"></span>,
                                                                                            что составляет
                                                                                            <span><input type="text" id="a43" name="a43" value="'''+str(work.a43)+'''"
                                                                                                         class="form-plan"></span>
                                                                                            %, при допуске 10 %.
                                                                                        </p>
                                                                                        <p>
                                                                                            Количество расхождений,
                                                                                            превышающих удвоенную
                                                                                            среднюю допустимую
                                                                                            погрешность
                                                                                            <span><input type="text" id="a44" name="a44" value="'''+str(work.a44)+'''"
                                                                                                         class="form-plan"></span>,
                                                                                            что составляет
                                                                                            <span><input type="text" id="a45" name="a45" value="'''+str(work.a45)+'''"
                                                                                                         class="form-plan"></span>
                                                                                            %, при допуске 5 %.
                                                                                        </p>
                                                                                        <b>Примечания:</b>
                                                                                        <p>
                                                                                            1. При углах наклона
                                                                                            местности до 20 допустимая
                                                                                            средняя ошибка по высоте
                                                                                            равна 12см.
                                                                                        </p>
                                                                                        <p>
                                                                                            2. При углах наклона
                                                                                            местности более 20
                                                                                            допустимая средняя ошибка по
                                                                                            высоте равна:
                                                                                        </p>
                                                                                        <p> – сечение рельефа через 0.5м
                                                                                            - 17см;</p>
                                                                                        <p> – сечение рельефа через 1м -
                                                                                            34см;</p>
                                                                                        <p> – сечение рельефа через 2м -
                                                                                            67см;</p>
                                                                                        <p> – сечение рельефа через 5м -
                                                                                            167см;</p>
                                                                                        <div class="mb-3 row">
                                                                                            <label class="col-sm-3 col-form-label">Оценка
                                                                                                качества горизонтальной
                                                                                                съемки:</label>
                                                                                            <div class="col-sm-9">
                                                                                                <input id="a46" name="a46" class="form-control" value="'''+str(work.a46)+'''"
                                                                                                       type="text"
                                                                                                       placeholder="">
                                                                                            </div>
                                                                                        </div>
                                                                                        <div class="mb-3 row">
                                                                                            <label class="col-sm-3 col-form-label">Замечания
                                                                                                по пропуску элементов
                                                                                                ситуации, правильности
                                                                                                применения условных
                                                                                                знаков:</label> '''+str(work.a47)+'''
                                                                                        </div>

                                                                                        <br><br>
                                                                                    </form>



                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div class="setup-content" id="step-3">
                                                                    <div class="col-xs-12">
                                                                        <div class="file-sidebar">
                                                                            <div class="pricing-plan">
                                                                                <div class="col-md-12">

                                                                                        <h4 class="m-t-20 text-center" style="text-align: center">2. полевого контроля и приемки работ по съемке инженерных сетей</h4>
                                                                                        <div class="mb-3 row">
                                                                                            <label class="col-sm-3 col-form-label">Мы, нижеподписавшиеся:</label> '''+str(work.a48)+'''
                                                                                        </div>
                                                                                        <p> составили настоящий акт в том, что за период с
                                                                                            <span><input type="text" class="form-plan" id="a49" value="'''+str(work.a49)+'''" name="a80"></span>
                                                                                            по
                                                                                            <span><input type="text" id="a50" name="a50" value="'''+str(work.a50)+'''" class="form-plan"></span>
                                                                                            20
                                                                                            <span><input type="text" id="a51" name="a51" value="'''+str(work.a51)+'''" class="form-plan"></span>
                                                                                            г.
                                                                                            произведен контроль и
                                                                                            приемка работ по съемке
                                                                                            инженерных сетей,
                                                                                            выполненных на объекте:
                                                                                        </p> '''+str(work.a52)+'''
                                                                                        <p>
                                                                                            № договор
                                                                                            <span><input type="text" id="a84" value="'''+str(work.a53)+'''" name="a53" class="form-plan m-t-10"></span>
                                                                                        </p>
                                                                                        <p>Соответствие объемов
                                                                                            выполненных работ указанным:
                                                                                            в пояснительной записке; в
                                                                                            программе работ.</p>
                                                                                        <h5 class="text-center f-w-700 m-b-20 m-t-20" style="text-align: center">
                                                                                            Результаты полевого
                                                                                            контроля:</h5>
                                                                                        <p>
                                                                                            Съемка инженерных сетей
                                                                                            проверена на
                                                                                            <span><input type="text" id="a54" value="'''+str(work.a54)+'''" name="a54"
                                                                                                         class="form-plan m-b-10"></span>
                                                                                            листах, и/или планшетах с
                                                                                            номенклатурой:
                                                                                        </p> '''+str(work.a55)+'''
                                                                                        <div class="col-sm-12 m-t-20">
                                                                                            <div class="card border-0">
                                                                                                <div class="table-responsive">
                                                                                                    <table class="table table-bordered"
                                                                                                           id="childTable5">
                                                                                                        <thead class="table-primary">
                                                                                                        <tr>
                                                                                                            <th scope="col">
                                                                                                                №
                                                                                                            </th>
                                                                                                            <th scope="col">Планшет (лист)
                                                                                                            </th>
                                                                                                            <th colspan="2" scope="col">Средняя ошибка (расхождение) в мм плана
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Расхождения,
                                                                                                                превышающие
                                                                                                                1,4мм
                                                                                                                плана в
                                                                                                                процентах
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Средняя
                                                                                                                ошибка
                                                                                                                (расхождение)
                                                                                                                в см по
                                                                                                                высоте
                                                                                                            </th>
                                                                                                            <th colspan="2"
                                                                                                                scope="col">
                                                                                                                Расхождения,
                                                                                                                превышающие
                                                                                                                удвоенное
                                                                                                                значение
                                                                                                                средней
                                                                                                                ошибки в
                                                                                                                проц.
                                                                                                            </th>
                                                                                                           
                                                                                                        </tr>
                                                                                                        </thead>
                                                                                                        <tbody>
                                                                                                        <tr>
                                                                                                            <th scope="row">
                                                                                                                1
                                                                                                            </th>
                                                                                                            <td><input id="a6_1" name="a6_1"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_1)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a6_2" name="a6_2"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_2)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a6_3" name="a6_3"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_3)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a6_4" name="a6_4"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_4)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a6_5" name="a6_5"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_5)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a6_6" name="a6_6"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_6)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a6_7" name="a6_7"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_7)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a6_8" name="a6_8"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_8)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            <td><input id="a6_9" name="a6_9"
                                                                                                                    class="border-0 w-100"
                                                                                                                    type="text" value="'''+str(work_table6.a6_9)+'''"
                                                                                                                    placeholder="">
                                                                                                            </td>
                                                                                                            
                                                                                                        </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div class="mb-3 row">
                                                                                            <label class="col-sm-3 col-form-label">Состояние
                                                                                                полевой и камеральной
                                                                                                документации:</label> '''+str(work.a56)+'''
                                                                                        </div>
                                                                                        <div class="mb-3 row">
                                                                                            <label class="col-sm-3 col-form-label">Замечания
                                                                                                по оформлению планшетов,
                                                                                                ЦТП:</label> '''+str(work.a57)+'''
                                                                                        </div>


                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div class="setup-content" id="step-4">
                                                                    <div class="col-xs-12">
                                                                        <div class="file-sidebar">
                                                                            <div class="pricing-plan">
                                                                                <div class="col-md-12">
                                                                                    <p class="text-end">ШНК
                                                                                        1.02.07-19 </p>
                                                                                    <p class="text-end">Приложение к
                                                                                        акту полевого контроля</p>
                                                                                     <h4 class="text-center f-w-600" style="text-align: center">
                                                                                        ВЕДОМОСТЬ</h4>
                                                                                    <h5 class="text-center f-w-600" style="text-align: center">
                                                                                        контрольных измерений
                                                                                        (план)</h5>

                                                                                        <h5 class="text-center f-w-600 m-t-20" style="text-align: center">
                                                                                        Контроль и оценка качества
                                                                                        съемки инженерных сетей</h5>

                                                                                    <div class="col-sm-12 m-t-5">
                                                                                        <div class="card border-0">
                                                                                            <div class="table-responsive">
                                                                                                <table class="table table-bordered"
                                                                                                       id="childTable6">
                                                                                                    <thead class="table-primary">
                                                                                                   <tr>
                                                                                                        <th scope="col">
                                                                                                            №
                                                                                                        </th>
                                                                                                        <th scope="col" class="text-center">
                                                                                                            Расстояния
                                                                                                            <br>
                                                                                                            с плана (м)
                                                                                                        </th>
                                                                                                        <th scope="col" class="text-center">
                                                                                                            Расстояния
                                                                                                            <br> в натуре м
                                                                                                        </th>
                                                                                                        <th scope="col" class="text-center">
                                                                                                            Расхождения
                                                                                                            <br>
                                                                                                            d,м
                                                                                                        </th>
                                                                                                        <th scope="col" class="text-center">
                                                                                                            Расхождения
                                                                                                            <br>
                                                                                                            d (мм) плана
                                                                                                        </th>
                                                                                                        <th scope="col" class="text-center">
                                                                                                            Между какими контурами и инженерными сооружениями произведены промеры
                                                                                                        </th>
                                                                                                        
                                                                                                    </tr>
                                                                                                    </thead>
                                                                                                    <tbody>
                                                                                                    <tr>
                                                                                                        <th scope="row">
                                                                                                            1
                                                                                                        </th>
                                                                                                        <td><input id="a7_1" name="a7_1" value="'''+str(work_table7.a7_1)+'''"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text"
                                                                                                                placeholder="">
                                                                                                        </td>
                                                                                                        <td><input id="a7_2" name="a7_2"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text" value="'''+str(work_table7.a7_2)+'''"
                                                                                                                placeholder="">
                                                                                                        </td>
                                                                                                        <td><input id="a7_3" name="a7_3"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text" value="'''+str(work_table7.a7_3)+'''"
                                                                                                                placeholder="">
                                                                                                        </td>
                                                                                                        <td><input id="a7_4" name="a7_4"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text" value="'''+str(work_table7.a7_4)+'''"
                                                                                                                placeholder="">
                                                                                                        </td>
                                                                                                        <td><input id="a7_5" name="a7_5"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text" value="'''+str(work_table7.a7_5)+'''"
                                                                                                                placeholder="">
                                                                                                        </td>
                                                                                                        
                                                                                                    </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </div>
                                                                                        </div>
                                                                                    </div>
                                                                                    <p>
                                                                                        Средняя погрешность положения на
                                                                                        плане инженерных сетей
                                                                                        d<sub>cp.</sub>=d/n
                                                                                        <span><input type="text" id="a58" value="'''+str(work.a58)+'''" name="a58"
                                                                                                     class="form-plan"></span>
                                                                                        мм, при допуске
                                                                                        <span><input type="text" id="a59" value="'''+str(work.a59)+'''" name="a59"
                                                                                                     class="form-plan"></span>
                                                                                        мм, по <span class="bg-warning">ШНК 1.02.08</span>
                                                                                    </p>
                                                                                    <p>
                                                                                        Количество предельных
                                                                                        расхождений (не более удвоенных
                                                                                        средних допустимых) получено
                                                                                        <span><input type="text" id="a60" name="a60" value="'''+str(work.a60)+'''"
                                                                                                     class="form-plan"></span>
                                                                                        , что составляет
                                                                                        <span><input type="text" id="a61" name="a61" value="'''+str(work.a61)+'''"
                                                                                                     class="form-plan"></span>
                                                                                        %, при допуске 10%.
                                                                                    </p>

                                                                                    <div class="mb-3 row">
                                                                                        <label class="col-sm-3 col-form-label">Оценка
                                                                                            качества плановой съемки
                                                                                            инженерных сетей</label>
                                                                                        <div class="col-sm-9">
                                                                                            <input class="form-control" id="a62" name="a62" value="'''+str(work.a62)+'''"
                                                                                                   type="text"
                                                                                                   >
                                                                                        </div>
                                                                                    </div>
                                                                                    <div class="mb-3 row">
                                                                                       Замечания
                                                                                            по пропуску элементов
                                                                                            инженерных сетей,
                                                                                            правильности применения
                                                                                            условных знаков: '''+str(work.a63)+'''

                                                                                    </div>
                                                                                    <div class="mb-3 row">
                                                                                        <label class="col-sm-3 col-form-label">Проверку
                                                                                            произвел(и) </label>
                                                                                        <div class="col-sm-9">
                                                                                            <input class="form-control" id="a64" value="'''+str(work.a64)+'''"  name="a64"
                                                                                                   type="text"
                                                                                                   >
                                                                                        </div>
                                                                                    </div>
                                                                                    <div class="mb-3 row">
                                                                                        <label class="col-sm-3 col-form-label">С
                                                                                            актом ознакомлен(ы)</label>
                                                                                        <div class="col-sm-9">
                                                                                            <input class="form-control" id="a65" value="'''+str(work.a65)+'''" name="65"
                                                                                                   type="text"
                                                                                                   >
                                                                                        </div>
                                                                                    </div>

                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div class="setup-content" id="step-5">
                                                                    <div class="col-xs-12">
                                                                        <div class="file-sidebar">
                                                                            <div class="pricing-plan">
                                                                                <div class="col-md-12">
                                                                                    <p class="text-end">ШНК
                                                                                        1.02.07-19 </p>
                                                                                    <p class="text-end">Приложение к
                                                                                        акту полевого контроля</p>
                                                                                    <h4 class="text-center f-w-600" style="text-align: center">
                                                                                        ВЕДОМОСТЬ</h4>
                                                                                    <h5 class="text-center f-w-600" style="text-align: center">
                                                                                        Контрольных
                                                                                        измерений-высота</h5>
                                                                                <h5 class="text-center f-w-600 m-t-20" style="text-align: center">
                                                                                        Контроль и оценка качества
                                                                                        съемки инженерных сетей</h5>

                                                                                    <div class="col-sm-12 m-t-5">
                                                                                        <div class="card border-0">
                                                                                            <div class="table-responsive">
                                                                                                <table class="table table-bordered"
                                                                                                       id="childTable7">
                                                                                                    <thead class="table-primary">
                                                                                                     <tr>
                                                                                                        <th scope="col">
                                                                                                            №
                                                                                                        </th>
                                                                                                        <th scope="col">
                                                                                                            Глубина заложения
                                                                                                            коммуникации
                                                                                                            <br>
                                                                                                            с плана см
                                                                                                        </th>
                                                                                                        <th scope="col">
                                                                                                            Глубина заложения
                                                                                                            коммуникации
                                                                                                            <br>
                                                                                                            в натуре cм
                                                                                                        </th>
                                                                                                        <th scope="col">
                                                                                                            Расхождения(h)
                                                                                                            <br>
                                                                                                            (гр.3-гр.2) см
                                                                                                        </th>

                                                                                                        <th scope="col">
                                                                                                           Описание местоположения
                                                                                                            контрольного замера
                                                                                                        </th>
                                                                                                        
                                                                                                    </tr>
                                                                                                    </thead>
                                                                                                    <tbody>
                                                                                                    <tr>
                                                                                                        <th scope="row">
                                                                                                            1
                                                                                                        </th>
                                                                                                        <td><input id="a8_1" name="a8_1"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text" value="'''+str(work_table8.a8_1)+'''"
                                                                                                                placeholder="">
                                                                                                        </td>
                                                                                                        <td><input id="a8_2" name="a8_2"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text" value="'''+str(work_table8.a8_2)+'''"
                                                                                                                placeholder="">
                                                                                                        </td>
                                                                                                        <td><input id="a8_3" name="a8_3"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text" value="'''+str(work_table8.a8_3)+'''"
                                                                                                                placeholder="">
                                                                                                        </td>
                                                                                                        <td><input id="a8_4" name="a8_4"
                                                                                                                class="border-0 w-100"
                                                                                                                type="text" value="'''+str(work_table8.a8_4)+'''"
                                                                                                             >
                                                                                                        </td>

                                                                                                        
                                                                                                    </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </div>
                                                                                        </div>
                                                                                    </div>

                                                                                    <p>
                                                                                        Предельные расхождения между
                                                                                        значениями глубин заложения
                                                                                        инженерных коммуникаций,
                                                                                        определенных во время
                                                                                        съемки с помощью приборов и
                                                                                        инструментов и по
                                                                                        данным контрольных полевых
                                                                                        измерений, не должны превышать
                                                                                        15% глубины заложения.
                                                                                    </p>

                                                                                    <p>
                                                                                        Средняя ошибка (расхождение) в
                                                                                        см по высоте h<sub>cp.</sub>=h/n
                                                                                        <span><input type="text" id="a66" name="a66" value="'''+str(work.a66)+'''}"
                                                                                                     class="form-plan"></span>
                                                                                        см, при допуске
                                                                                        <span><input type="text" id="a122" name="a67" value="'''+str(work.a67)+'''"
                                                                                                     class="form-plan"></span>
                                                                                        см.
                                                                                    </p>

                                                                                    <div class="mb-3 row">
                                                                                        <label class="col-sm-3 col-form-label">Оценка
                                                                                            качества плановой съемки
                                                                                            инженерных сетей</label>
                                                                                        <div class="col-sm-9">
                                                                                            <input class="form-control" id="a68" name="a68" value="'''+str(work.a68)+'''"
                                                                                                   type="text"
                                                                                                   >
                                                                                        </div>
                                                                                    </div>

                                                                                    <div class="mb-3 row">
                                                                                        Замечания '''+str(work.a69)+'''

                                                                                    </div>

                                                                                    <div class="mb-3 row">
                                                                                        <label class="col-sm-3 col-form-label">Проверку
                                                                                            произвел(и) </label>
                                                                                        <div class="col-sm-9">
                                                                                            <input class="form-control" id="a70" name="a70" value="'''+str(work.a70)+'''"
                                                                                                   type="text"
                                                                                                   >
                                                                                        </div>
                                                                                    </div>

                                                                                    <div class="mb-3 row">
                                                                                        <label class="col-sm-3 col-form-label">С
                                                                                            актом ознакомлен(ы)</label>
                                                                                        <div class="col-sm-9">
                                                                                            <input class="form-control" id="a71" name="a71" value="'''+str(work.a71)+'''"
                                                                                                   type="text"
                                                                                                   >
                                                                                        </div>
                                                                                    </div>


                                                                                </div>



                                                                            </div>



                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                </form>
    </div>

</body>

</html>
               ''';

        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
            'orientation': 'portrait',
            # landscape bu albomiy qiladi
        }
        # display = Display(visible=0, size=(500, 500)).start()
        pdfkit.from_string(context, 'topografiya/static/files/akt_polevoy/akt-polevoy.pdf', options)

        response = HttpResponse(data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="akt-polevoy.pdf"'
        return response
    else:
        return HttpResponse(0)

def show_pdowork(request,id):
    pdowork = PdoWork.objects.filter(id=id).first()
    workers=Worker.objects.filter(branch=pdowork.branch).filter(status=0)
    context = {'pdowork': pdowork, 'workers': workers,'count': counter()}
    return render(request, 'leader/show_pdowork.html', context)

def edit_pdowork(request,id):

    pdowork = PdoWork.objects.filter(id=id).filter(status_recive=1).first()
    workers=Worker.objects.filter(branch=pdowork.branch).filter(status=0)
    order = Order.objects.filter(object__pdowork=pdowork).first()
    object=Object.objects.filter(pdowork=pdowork).first()
    context = {'pdowork': pdowork, 'workers': workers, 'order': order,'object':object,'count': counter()}
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
        worker_ispolnitel = request.POST.get('worker_ispolnitel')

        pdowork = PdoWork.objects.filter(id=pdowork).first()
        pdowork.status_recive=1
        # status_recive = 1 is started work but not recived by worker
        pdowork.save()

        object = Object(pdowork=pdowork, worker_leader=order_creator, isset_programwork=is_programwork,worker_ispolnitel = worker_ispolnitel)
        object.save()

        order = Order(object=object,info=info,method_creation=method_creation,method_fill=method_fill,syomka=syomka,requirements=requirements,item_check=item_check,
                     list_of_materials=list_of_materials,adjustment_methods=adjustment_methods,type_of_sirie=type_of_sirie,order_creator=order_creator,order_receiver=worker_ispolnitel)
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
        object.worker_leader = worker_id
        object.isset_programwork = is_programwork
        object.worker_ispolnitel = worker_ispolnitel
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

# geodezis
def program_works_geodezis(request):
    new_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=1).all()

    rejected_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=2).all()
    rejecteds = ProgramWorkReject.objects.all()
    less_time_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=3).all()
    aggreed_ones = ProgramWork.objects.filter(object__isset_programwork=True).filter(status=4).all()

    context = {'new_ones': new_ones,'rejected_ones': rejected_ones, 'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones,'count': counter(),
               'rejecteds': rejecteds}
    # print(objects)
    return render(request, 'geodezis/program_works_geodesiz.html', context)

def program_work_event(request, id):
    object = ProgramWorkForm.objects.filter(programwork__object=id).first()
    order = Order.objects.filter(object=object.programwork.object.id).first()
    workers = Worker.objects.filter(branch=object.programwork.object.pdowork.branch)
    formtable1 = ProgramWorkFormTable1.objects.filter(programworkform=object).first()
    formtable2 = ProgramWorkFormTable2.objects.filter(programworkform=object).first()
    files = ProgramWorkFiles.objects.filter(programworkform=object).first()

    rejects = ProgramWorkReject.objects.filter(programowork=object.programwork).all()

    context = {'object': object, 'order': order, 'workers': workers, 'formtable2':formtable2, 'formtable1': formtable1, 'count': counter(), 'rejects': rejects,'files': files}
    return render(request, 'geodezis/program_work_event.html', context)

def confirm_program_work(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('object-id')
        worker = data.get('worker')

        object = ProgramWork.objects.filter(object=id).first()
        object.status = 4
        object.save()

        object_id = Object.objects.filter(id=object.object.id).first()
        worker1 = Object.objects.filter(id=id).first()
        worker1.worker_geodezis = worker
        worker1.save()

        history = History(object=object_id, status=4, comment="Tasdiqlandi", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def reject_program_work(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('object-id')
        worker = data.get('worker')
        reason = data.get('reason')
        reject_file =request.FILES.get('reject_file')

        object = ProgramWork.objects.filter(object=id).first()
        object.status = 2
        object.save()

        object_id = Object.objects.filter(id=object.object.id).first()

        reject = ProgramWorkReject(programowork=object, file=reject_file, reason=reason)
        reject.save()

        history = History(object=object_id, status=5, comment="Rad etildi", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)
def program_work_form_re_sent(request,id):
    if request.method == 'POST':
        a0 = request.POST.get('a0')
        a1_1 = request.POST.get('a1_1')
        a1_2 = request.POST.get('a1_2')
        a1_3 = request.POST.get('a1_3')

        a2 = request.POST.get('a2')
        a3 = request.POST.get('a3')
        a4 = request.POST.get('a4')
        a5 = request.POST.get('a5')
        a6 = request.POST.get('a6')


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

        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        file3 = request.FILES.get('file3')
        file4 = request.FILES.get('file4')
        file5 = request.FILES.get('file5')
        file6 = request.FILES.get('file6')
        file7 = request.FILES.get('file7')

        program_work_creator = request.POST.get('program_work_creator')

        object = Object.objects.filter(id=id).first()
        programwork=ProgramWork.objects.filter(object=id).first()

        form = ProgramWorkForm.objects.filter(programwork=programwork).first()

        form.programwork=programwork
        form.a0=a0
        form.a1_1=a1_1
        form.a1_2 = a1_2
        form.a1_3 = a1_3
        form.a2 = a2
        form.a3 = a3
        form.a4 = a4
        form.a5 = a5
        form.a6=a6
        form.a7_2=a7_2
        form.a7_3=a7_3
        form.a7_4=a7_4
        form.a8=a8
        form.a8_1=a8_1
        form.a9_1=a9_1
        form.a9_3=a9_3
        form.a9_4=a9_4
        form.a10=a10
        form.a11=a11
        form.a12=a12
        form.program_work_creator=program_work_creator
        form.save()

        formtable1 = ProgramWorkFormTable1.objects.filter(programworkform=form).first()
        formtable1.programworkform=form
        formtable1.a7_1_1=a7_1_1
        formtable1.a7_1_2=a7_1_2
        formtable1.a7_1_3=a7_1_3
        formtable1.a7_1_4=a7_1_4
        formtable1.a7_1_5=a7_1_5
        formtable1.save()

        formtable2 = ProgramWorkFormTable2.objects.filter(programworkform=form).first()
        formtable2.programworkform=form
        formtable2.a9_2_1=a9_2_1
        formtable2.a9_2_2=a9_2_2
        formtable2.a9_2_3=a9_2_3
        formtable2.a9_2_4=a9_2_4
        formtable2.a9_2_5=a9_2_5
        formtable2.a9_2_6=a9_2_6
        formtable2.a9_2_7=a9_2_7
        formtable2.save()

        files = ProgramWorkFiles.objects.filter(programworkform=form).first()
        if file1:
            files.file1 = file1
        else:
            files.file1 = files.file1

        if file2:
            files.file2 = file2
        else:
            files.file2 = files.file2

        if file3:
            files.file3 = file3
        else:
            files.file3 = files.file3

        if file4:
            files.file4 = file4
        else:
            files.file4 = files.file4

        if file5:
            files.file1 = file5
        else:
            files.file5 = files.file5

        if file6:
            files.file6 = file6
        else:
            files.file6 = files.file6

        if file7:
            files.file6 = file7
        else:
            files.file7 = files.file7

        files.save()

        programwork = ProgramWork.objects.filter(object=id).first()
        programwork.status = 1
        programwork.save()
        # status  = 1 bu tekshiruvga yuborilgan
        history = History(object=object, status=6, comment="Topografik geodezik ish tekshiruvga qayta yuborildi", user_id = program_work_creator)
        # status=6 bu qayta tekshiruvga yuborildi
        history.save()

        # messages.success(request, "Ish tekshiruvga yuborildi !")
        return HttpResponseRedirect('/program_works_leader')

def geodesiz_komeral_works(request):
    # status_recive = 1 is started work but not recived by worker
    checking_ones = WorkerObject.objects.filter(status_geodezis_komeral=1).all()  # dala nazorati muhokama jarayonida
    rejected_ones = WorkerObject.objects.filter(status_geodezis_komeral=2).all()  # qaytarilgan ishlar
    less_time_ones = WorkerObject.objects.filter(status_geodezis_komeral=3).all()  # muddati kam qolgan ishlar
    aggreed_ones =WorkerObject.objects.filter(status_geodezis_komeral=4).all()  # tasdiqlangan ishlar
    rejecteds = LeaderKomeralWorkReject.objects.all()

    context = {'worker_new_works': worker_new_works, 'checking_ones': checking_ones, 'rejected_ones': rejected_ones,
               'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones, 'count': counter(),
               'rejecteds': rejecteds}
    return render(request, 'geodezis/head_komeral/komeral_works.html', context)

def show_geodesiz_kameral_work(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    rejects = LeaderKomeralWorkReject.objects.filter(object=workerobject.object).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(),'order':order,'work':work,'rejects':rejects,'sirie_type':sirie_type,
               'siriefiles': sirie_files,'aktkomeral':aktkomeral,'programwork':programwork}

    return render(request, 'geodezis/head_komeral/checking_komeral_works.html', context)

def geodezis_deny_komeral(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')
        reason = data.get('reason')
        reason_file =request.FILES.get('reason_file')

        workerobject = WorkerObject.objects.filter(object=work_id).first()
        workerobject.status_geodezis_komeral = 2
        workerobject.save()


        reject = LeaderKomeralWorkReject(object=workerobject.object, file=reason_file, reason=reason)
        reject.save()

        history = History(object=workerobject.object, status=18, comment="Komeral nazorat bosh geodezis tomonidan red etildi", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)


def geodezis_rejected_komeral_works(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()

    aktkomeral = AktKomeralForm.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    rejects = LeaderKomeralWorkReject.objects.filter(object=workerobject.object).all()
    context = {'workerobject': workerobject, 'pdowork': pdowork, 'count': counter(), 'order': order, 'work': work, 'rejects': rejects, 'sirie_type': sirie_type,
               'siriefiles': sirie_files,'aktkomeral': aktkomeral, 'programwork': programwork}

    return render(request, 'geodezis/head_komeral/rejected_komeral_works.html', context)


def sent_to_oggd(request):
    if request.method == 'POST':
        data = request.POST
        work_id = data.get('work_id')
        worker = data.get('worker')

        workerobject=WorkerObject.objects.filter(object=work_id).first()
        workerobject.status_geodezis_komeral=4
        workerobject.save()

        object = Object.objects.filter(id=work_id).first()
        object.worker_geodezis = worker
        object.save()

        if object.isset_programwork == True:
            report = Report(object=object)
            report.save()

        history = History(object=object, status=20, comment="Komeral nazorat bosh geodezis tomonidan tasdiqlandi", user_id=worker)
        history.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def geodeziz_show_komeral_work(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    rejects = LeaderKomeralWorkReject.objects.filter(object=workerobject.object).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork, 'count': counter(),'order':order,'work':work,'rejects':rejects,'sirie_type':sirie_type,
               'siriefiles': sirie_files,'aktkomeral':aktkomeral, 'programwork': programwork}

    return render(request, 'geodezis/head_komeral/show_komeral_work.html', context)


def geodezis_reports(request):
    new_ones = Report.objects.filter(status=0).all()
    checking_ones = Report.objects.filter(status=1).all()
    rejected_ones = Report.objects.filter(status=2).all()
    less_time_ones = Report.objects.filter(status=3).all()
    aggreed_ones = Report.objects.filter(status=4).all()
    rejecteds = ReportReject.objects.all()
    context = {'new_ones': new_ones,'rejected_ones': rejected_ones, 'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones,'count': counter(),
               'rejecteds': rejecteds,'checking_ones': checking_ones}
    # print(objects)
    return render(request, 'geodezis/report/reports.html', context)

def geodezis_report_checking(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    rejects = ReportReject.objects.filter(object=workerobject.object).all()
    report = Report.objects.filter(object=id).last()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(),'order':order,'work':work,'rejects':rejects,'sirie_type':sirie_type,
               'siriefiles': sirie_files,'aktkomeral':aktkomeral,'report':report,'programwork': programwork}

    return render(request, 'geodezis/report/report_checking.html', context)

def show_report_geodezis(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()

    rejects = ReportReject.objects.filter(object=workerobject.object).all()
    report = Report.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(),'order':order,'work':work,'rejects':rejects,'sirie_type':sirie_type,
               'siriefiles': sirie_files,'aktkomeral':aktkomeral,'report':report,'programwork': programwork}

    return render(request, 'geodezis/report/show_report.html', context)

def reject_report(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('work_id')
        worker = data.get('worker')
        reason = data.get('reason')
        reason_file =request.FILES.get('reason_file')

        report = Report.objects.filter(object=id).first()
        report.status = 2
        report.save()

        work = ReportReject(object=report.object, file=reason_file,reason=reason)
        work.save()

        history = History(object=report.object, status=22, comment="Geodezis xisoborni rad etgan!", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def confirm_report(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('work_id')
        worker = data.get('worker')


        report = Report.objects.filter(object=id).first()
        report.status = 4
        report.save()

        history = History(object=report.object, status=23, comment="Geodezis xisoborni tasdiqlandi!", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

# geodezis

# oogd_reports
def oogd_reports(request):
    new_ones = Report.objects.filter(status=0).all()
    checking_ones = Report.objects.filter(status=1).all()
    rejected_ones = Report.objects.filter(status=2).all()
    less_time_ones = Report.objects.filter(status=3).all()
    aggreed_ones = Report.objects.filter(status=4).all()
    rejecteds = ReportReject.objects.all()
    context = {'new_ones': new_ones,'rejected_ones': rejected_ones, 'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones,'count': counter(),
               'rejecteds': rejecteds,'checking_ones': checking_ones}
    # print(objects)
    return render(request, 'oogd_reporter/report/reports.html', context)

def report_doing(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    rejects = ReportReject.objects.filter(object=workerobject.object).all()
    reports = Report.objects.filter(object=id).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork, 'count': counter(),'order':order,'work':work,'rejects':rejects,'sirie_type':sirie_type,
               'siriefiles': sirie_files,'aktkomeral':aktkomeral, 'programwork': programwork,'reports':reports}

    return render(request, 'oogd_reporter/report/report_doing.html', context)

def report_send(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('work_id')
        worker = data.get('worker')
        reason = data.get('reason')
        report_file =request.FILES.get('report_file')

        report = Report.objects.filter(object=id).first()
        report.status = 1
        report.file = report_file
        report.reason = reason
        report.save()

        object = Object.objects.filter(id=id).first()
        object.worker_ogogd = worker
        object.save()

        history = History(object=report.object, status=21, comment="Oogd xodimi hisobotni tekshiruvga yubordi", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def show_report(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()

    programwork = ProgramWork.objects.filter(object=id).first()

    rejects = ReportReject.objects.filter(object=workerobject.object).all()
    reports = Report.objects.filter(object=id).all()
    print(reports)
    context = {'workerobject': workerobject, 'pdowork': pdowork, 'count': counter(), 'order':order, 'work':work, 'rejects':rejects, 'sirie_type':sirie_type,
               'siriefiles': sirie_files, 'aktkomeral':aktkomeral, 'reports': reports, 'programwork': programwork}

    return render(request, 'oogd_reporter/report/show_report.html', context)

def sent_to_print(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()
    programwork = ProgramWork.objects.filter(object=id).first()
    rejects = ReportReject.objects.filter(object=workerobject.object).all()
    report = Report.objects.filter(object=id).first()

    context = {'workerobject': workerobject, 'pdowork': pdowork, 'count': counter(), 'order': order, 'work': work,
               'rejects': rejects, 'sirie_type': sirie_type,
               'siriefiles': sirie_files, 'aktkomeral': aktkomeral, 'report': report,'programwork':programwork}

    return render(request, 'oogd_reporter/report/sent_to_print.html', context)

def confirm_print(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('work_id')
        worker = data.get('worker')

        report = Report.objects.filter(object=id).first()
        report.status = 5
        report.save()

        workerobject = WorkerObject.objects.filter(object=report.object).first()
        workerobject.status = 5
        workerobject.status_geodezis_komeral = 5
        workerobject.save()

        aktkomeral = AktKomeralForm.objects.filter(object=report.object).first()
        aktkomeral.status = 5
        aktkomeral.save()

        programwork = ProgramWork.objects.filter(object=report.object).first()
        programwork.status=5
        programwork.save()

        history = History(object=report.object, status=24, comment="Obektni pechatga yuborish", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

# oogd_reports

# ogogd_printer

def ogogd_printer_works(request):
    works = WorkerObject.objects.filter(status_geodezis_komeral=4).all()
    context = {'count': counter(),'works': works}

    return render(request, 'oogd_printer/works.html', context)

def open_to_print(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()

    programwork = ProgramWork.objects.filter(object=id).first()

    rejects_reports = ReportReject.objects.filter(object=workerobject.object).all()
    rejects_programworks = ProgramWorkReject.objects.filter(programowork=programwork).all()
    rejects_akt_polevoy_works = PolevoyWorkReject.objects.filter(workerobject=workerobject).all()
    rejects_akt_komeral_works = KameralWorkReject.objects.filter(workerobject=pdowork).all()
    rejects_akt_komeral_leader_works = LeaderKomeralWorkReject.objects.filter(object=pdowork).all()

    sum = int(rejects_programworks.count()) + int(rejects_reports.count()) + int(
        rejects_akt_komeral_works.count()) + int(rejects_akt_polevoy_works.count()) + int(
        rejects_akt_komeral_leader_works.count())

    report = Report.objects.filter(object=id).all()

    context = {'workerobject': workerobject, 'pdowork': pdowork, 'count': counter(), 'order': order, 'work': work,
               'rejects_reports': rejects_reports,
               'rejects_programworks': rejects_programworks, 'rejects_akt_polevoy_works': rejects_akt_polevoy_works,
               'rejects_akt_komeral_works': rejects_akt_komeral_works,
               'rejects_akt_komeral_leader_works': rejects_akt_komeral_leader_works,
               'sirie_type': sirie_type, 'siriefiles': sirie_files, 'aktkomeral': aktkomeral, 'reports': report,
               'sum': sum, 'programwork': programwork}

    return render(request, 'oogd_printer/show.html', context)

def confirm_print2(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('work_id')
        worker = data.get('worker')

        object = Object.objects.filter(id=id).first()

        workerobject = WorkerObject.objects.filter(object=object).first()
        workerobject.status = 5
        workerobject.status_geodezis_komeral = 5
        workerobject.save()

        aktkomeral = AktKomeralForm.objects.filter(object=workerobject.object).first()
        aktkomeral.status = 5
        aktkomeral.save()
        object = Object.objects.filter(id=workerobject.object).first()
        object.worker_ogogd = worker
        object.save()

        history = History(object=workerobject.object, status=22, comment="Obektni pechatga yuborish hisobotsiz", user_id=worker)
        history.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

# ogogd_printer
def history(request):
    works = WorkerObject.objects.filter(status = 5).order_by('-id').all()
    content={'count': counter(),'works':works}
    return render(request,'history.html',content)
def workers(request):
    workers = Worker.objects.filter(status=0).all()
    objects = Object.objects.all()
    workerobjects = WorkerObject.objects.all()
    content={'count': counter(), 'workers': workers, 'objects': objects, 'workerobjects':workerobjects}

    return render(request,'leader/workers.html', content)

def show_all_works(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()

    order = Order.objects.filter(object=id).first()

    work = WorkerObject.objects.filter(object=id).first()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()
    aktkomeral = AktKomeralForm.objects.filter(object=id).first()

    programwork = ProgramWork.objects.filter(object=id).first()

    rejects_reports = ReportReject.objects.filter(object=workerobject.object).all()
    rejects_programworks = ProgramWorkReject.objects.filter(programowork=programwork).all()
    rejects_akt_polevoy_works = PolevoyWorkReject.objects.filter(workerobject=workerobject).all()
    rejects_akt_komeral_works = KameralWorkReject.objects.filter(workerobject=pdowork).all()
    rejects_akt_komeral_leader_works = LeaderKomeralWorkReject.objects.filter(object=pdowork).all()

    sum = int(rejects_programworks.count())+int(rejects_reports.count())+int(rejects_akt_komeral_works.count())+int(rejects_akt_polevoy_works.count())+int(rejects_akt_komeral_leader_works.count())

    report = Report.objects.filter(object=id).all()


    context = {'workerobject': workerobject, 'pdowork': pdowork, 'count': counter(), 'order':order, 'work': work, 'rejects_reports':rejects_reports,
               'rejects_programworks': rejects_programworks, 'rejects_akt_polevoy_works': rejects_akt_polevoy_works,
               'rejects_akt_komeral_works': rejects_akt_komeral_works,'rejects_akt_komeral_leader_works':rejects_akt_komeral_leader_works,
               'sirie_type': sirie_type, 'siriefiles': sirie_files, 'aktkomeral': aktkomeral, 'reports': report,'sum':sum,'programwork':programwork}

    return render(request, 'show.html', context)


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
