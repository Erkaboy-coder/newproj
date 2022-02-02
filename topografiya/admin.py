from django.contrib import admin

# Register your models here.
from topografiya.models import Worker, Department, PdoWork, ProgramWorkForm, ProgramWork, Order, \
    AktKomeralForm, AktPolevoyForm, History, Object, WorkerObject, Branch, ProgramWorkFormTable1, ProgramWorkFormTable2, \
    SirieFiles, PoyasitelniyForm

admin.site.register(Worker)
admin.site.register(Object)
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
admin.site.register(ProgramWorkFormTable1)
admin.site.register(ProgramWorkFormTable2)

admin.site.register(SirieFiles)
admin.site.register(PoyasitelniyForm)
