from django.contrib import admin

# Register your models here.
from topografiya.models import Worker, Department, PdoWork, ProgramWorkForm, ProgramWork, Order, \
    AktKomeralForm, AktPolevoyForm, History, Object, WorkerObject, Branch, ProgramWorkFormTable1, ProgramWorkFormTable2, \
    SirieFiles, PoyasitelniyForm, PoyasitelniyFormTable2, PoyasitelniyFormTable1, PoyasitelniyFormTable3, \
    PoyasitelniyFormTable4, AktPolovoyTable1, AktPolovoyTable2, AktPolovoyTable3, AktPolovoyTable4, AktPolovoyTable5, \
    AktPolovoyTable6, AktPolovoyTable7, AktPolovoyTable8, PolevoyWorkReject,ProgramWorkReject,KameralWorkReject

admin.site.register(Worker)
admin.site.register(Object)
admin.site.register(Branch)
admin.site.register(Department)
admin.site.register(PdoWork)
admin.site.register(ProgramWorkForm)
admin.site.register(ProgramWork)
admin.site.register(Order)
admin.site.register(AktKomeralForm)
admin.site.register(KameralWorkReject)

admin.site.register(AktPolevoyForm)
admin.site.register(WorkerObject)
admin.site.register(History)
admin.site.register(ProgramWorkFormTable1)
admin.site.register(ProgramWorkFormTable2)
admin.site.register(ProgramWorkReject)

admin.site.register(SirieFiles)
admin.site.register(PoyasitelniyForm)
admin.site.register(PoyasitelniyFormTable1)
admin.site.register(PoyasitelniyFormTable2)
admin.site.register(PoyasitelniyFormTable3)
admin.site.register(PoyasitelniyFormTable4)

admin.site.register(AktPolovoyTable1)
admin.site.register(AktPolovoyTable2)
admin.site.register(AktPolovoyTable3)
admin.site.register(AktPolovoyTable4)
admin.site.register(AktPolovoyTable5)
admin.site.register(AktPolovoyTable6)
admin.site.register(AktPolovoyTable7)
admin.site.register(AktPolovoyTable8)
admin.site.register(PolevoyWorkReject)



