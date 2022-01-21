from django.contrib import admin

# Register your models here.
from topografiya.models import Worker, Department, PdoWork, ProgramWorkForm, ProgramWork, Order, \
    AktKomeralForm, AktPolevoyForm, History, Object,WorkerObject,Branch

admin.site.register(Worker)
admin.site.register(Branch)
admin.site.register(Department)
admin.site.register(PdoWork)
admin.site.register(ProgramWorkForm)
admin.site.register(ProgramWork)
admin.site.register(Order)
admin.site.register(AktKomeralForm)
admin.site.register(AktPolevoyForm)
admin.site.register(WorkerObject)
admin.site.register(History)
admin.site.register(Object)