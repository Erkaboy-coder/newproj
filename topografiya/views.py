from django.shortcuts import render,redirect
from .models import Branch, PdoWork, Worker, Order, Object, History, ProgramWork, ProgramWorkForm, \
    ProgramWorkFormTable1, ProgramWorkFormTable2, WorkerObject, ProgramWorkReject, SirieFiles, PoyasitelniyForm, \
    PoyasitelniyFormTable1, PoyasitelniyFormTable2, PoyasitelniyFormTable3, PoyasitelniyFormTable4
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

def counter():
    count = {}
    count['new_workers_pdo'] = PdoWork.objects.filter(status_recive=0).all().count()
    count['new_works_worker'] = PdoWork.objects.filter(status_recive=1).all().count()

    count['new_field_works'] = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=0).all().count()

    count['new_works_geodezis'] = ProgramWork.objects.filter(status=1).all().count()
    count['new_program_works_leader'] = ProgramWork.objects.filter(status=0).all().count()
    count['new_polevoy_works_leader'] = WorkerObject.objects.filter(status=1).all().count()

    return count

@login_required(login_url='/signin')
def index(request):
    context = {'count': counter()}
    return render(request, 'index.html', context)

def pdoworks(request):
    pdoworks = PdoWork.objects.filter(status=0).filter(~Q(status_recive=2))
    context = {'pdoworks': pdoworks,'count': counter()}
    return render(request, 'leader/pdo_works.html', context)

def allworks(request):
    pdoworks = PdoWork.objects.filter(status=0)

    context = {'pdoworks': pdoworks,'count': counter()}
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
    return render(request, 'leader/program_works.html', context)

def program_work_form(request,id):

    object = ProgramWork.objects.filter(object=id).first()
    order = Order.objects.filter(object=object.id).first()
    workers = Worker.objects.filter(branch=object.object.pdowork.branch)

    context = {'object': object, 'order': order, 'workers': workers,'count': counter()}
    return render(request, 'leader/program_work_form.html', context)

def program_work_form_edit(request,id):

    object = Object.objects.filter(id=id).first()
    form = ProgramWorkForm.objects.filter(programwork__object=id).first()
    formtable1 = ProgramWorkFormTable1.objects.filter(programworkform=form).first()
    formtable2 = ProgramWorkFormTable2.objects.filter(programworkform=form).first()

    rejects = ProgramWorkReject.objects.filter(programowork=form.programwork).first()

    order = Order.objects.filter(object=object.id).first()
    workers = Worker.objects.filter(branch=object.pdowork.branch)


    context = {'object': object, 'order': order, 'workers': workers, 'form': form, 'rejects':rejects,
               'formtable1':formtable1,'formtable2':formtable2,'count': counter()}
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

        programworkformtable2 = ProgramWorkFormTable2(programworkform=programworkform, a9_2_1=a9_2_1, a9_2_2=a9_2_2, a9_2_3=a9_2_3, a9_2_4=a9_2_4, a9_2_5=a9_2_5, a9_2_6=a9_2_6, a9_2_7=a9_2_7)
        programworkformtable2.save()


        # messages.success(request, "Ish tekshiruvga yuborildi !")
        return HttpResponseRedirect('/program_works_leader')

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

    context = {'worker_new_works': worker_new_works, 'checking_ones': checking_ones, 'rejected_ones': rejected_ones,
               'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones,'count': counter()}
    return render(request, 'leader/polevoy_works.html', context)

def checking_polevoy_works(request,id):
    workerobject = WorkerObject.objects.filter(object=id).first()
    pdowork = Object.objects.filter(id=id).first()
    siriefiles = SirieFiles.objects.filter(workerobject=workerobject).first()
    order = Order.objects.filter(object=id).first()

    context = {'workerobject': workerobject, 'pdowork': pdowork,'count': counter(), 'siriefiles': siriefiles,'order':order}

    return render(request, 'leader/checking_polevoy_works.html', context)

# leader


# worker
def worker_new_works(request):
    # status_recive = 1 is started work but not recived by worker
    worker_new_works = Object.objects.filter(pdowork__status_recive=1).all()

    context = {'worker_new_works': worker_new_works, 'count': counter()}
    return render(request, 'worker/worker_new_works.html', context)

def polevoy_works(request):
    # status_recive = 1 is started work but not recived by worker
    new_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=0).all() # yangi kelgan
    checking_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=1).all() # muhokama jarayonida
    rejected_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=2).all() # qaytarilgan ishlar
    less_time_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=3).all() # muddati kam qolgan ishlar
    aggreed_ones = WorkerObject.objects.filter(object__pdowork__status_recive=2).filter(status=4).all() # tasdiqlangan ishlar

    context = {'worker_new_works': worker_new_works,'new_ones': new_ones, 'checking_ones': checking_ones, 'rejected_ones': rejected_ones,
               'less_time_ones': less_time_ones, 'aggreed_ones': aggreed_ones,'count': counter()}
    return render(request, 'worker/polevoy_works.html', context)

def polevoy_work_doing(request,id):
    work = WorkerObject.objects.filter(object=id).first()
    objects = PdoWork.objects.filter(status_recive=1).all()
    objects_pdo = PdoWork.objects.filter(status_recive=0).all()
    sirie_type = Order.objects.filter(object=work.object.id).first()

    sirie_files = SirieFiles.objects.filter(workerobject=work).first()

    context = {'worker_new_works': worker_new_works, 'objects': objects, 'work':work,'objects_pdo': objects_pdo, 'sirie_type':sirie_type,
               'file': sirie_files,'count': counter()}
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

        history = History(object=object_id, status=7, comment="Dala nazoratiga sirie ma'lumotlari yuklandi", user_id=worker)
        history.save()

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
        print(file3_2)
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
        workerobject.file1_1=file1_1
        workerobject.file1_2=file1_2
        workerobject.file1_3=file1_3
        workerobject.file1_4=file1_4
        workerobject.file1_5=file1_5
        workerobject.file1_6=file1_6
        workerobject.file1_7=file1_7
        workerobject.file1_8=file1_8
        workerobject.file1_9=file1_9
        workerobject.file1_10=file1_10
        workerobject.file1_11=file1_11

        workerobject.file2_1=file2_1
        workerobject.file2_2=file2_2
        workerobject.file2_3=file2_3
        workerobject.file2_4=file2_4
        workerobject.file2_5=file2_5
        workerobject.file2_6=file2_6
        workerobject.file2_7=file2_7

        workerobject.file3_1=file3_1
        workerobject.file3_2=file3_2
        workerobject.file3_3=file3_3
        workerobject.file3_4=file3_4
        workerobject.file3_5=file3_5
        workerobject.file3_6=file3_6
        workerobject.file3_7=file3_7
        workerobject.file3_8=file3_8
        workerobject.file3_9=file3_9
        workerobject.file3_10=file3_10
        workerobject.save()

        object_id = Object.objects.filter(id=object.object.id).first()

        history = History(object=object_id, status=7, comment="Dala nazoratiga sirie ma'lumotlari yuklandi", user_id=worker)
        history.save()

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

        form1 = PoyasitelniyForm(workerobject=workerobject,b1=b1,b2=b2,b_1=b_1,b_2=b_2,b3=b3,b3_1=b3_1,b4=b4,b5=b5,b6=b6,b7=b7,b8_1_1=b8_1_1,b10=b10,b11=b11,b12=b12
                                 ,b13=b13,b14=b14,b15=b15,b16_a=b16_b,b19=b19,b19_1=b19_1,b19_2=b19_2,b20=b20,b21=b21,c_1=c_1,c_2=c_2,c_3=c_3,c_4=c_4,c_5=c_5,c_6=c_6
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
        form1.b16_a=b16_b
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


        object = WorkerObject.objects.filter(id=id).first()

        if object.abris_file == '':
            object.abris_file = abris
        else:
            object.abris_file = object.abris_file

        if object.kroki_file == '':
            object.kroki_file = kroki
        else:
            object.kroki_file = object.kroki_file


        if object.jurnal_file == '':
            object.jurnal_file = jurnal
        else:
            object.jurnal_file = object.jurnal_file

        if object.vidimes_file == '':
            object.vidimes_file = vidimes
        else:
            object.vidimes_file = object.vidimes_file

        if object.list_agreement_file == '':
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

    context = {'worker_new_works': worker_new_works, 'objects': objects, 'work':work, 'objects_pdo': objects_pdo,'sirie_type':sirie_type,'count': counter(),
               'form':form, 'form1':form1, 'form2':form2, 'form3':form3, 'form4':form4
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

# worker

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

def show_pdowork(request,id):
    pdowork = PdoWork.objects.filter(id=id).first()
    workers=Worker.objects.filter(branch=pdowork.branch)
    context = {'pdowork': pdowork, 'workers': workers,'count': counter()}
    return render(request, 'leader/show_pdowork.html', context)

def edit_pdowork(request,id):

    pdowork = PdoWork.objects.filter(id=id).filter(status_recive=1).first()
    workers=Worker.objects.filter(branch=pdowork.branch)
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

    context = {'object': object, 'order': order, 'workers': workers,'formtable2':formtable2,'formtable1':formtable1,'count': counter()}
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
        form.a7=a7
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

        programwork = ProgramWork.objects.filter(object=id).first()
        programwork.status = 1
        programwork.save()
        # status  = 1 bu tekshiruvga yuborilgan
        history = History(object=object, status=6, comment="Topografik geodezik ish tekshiruvga qayta yuborildi", user_id = program_work_creator)
        # status=6 bu qayta tekshiruvga yuborildi
        history.save()

        # messages.success(request, "Ish tekshiruvga yuborildi !")
        return HttpResponseRedirect('/program_works_leader')

# geodezis


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
