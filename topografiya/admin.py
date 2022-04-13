from django.contrib import admin
from leaflet.admin  import LeafletGeoAdmin

# Register your models here.
from topografiya.models import *


class PointsAdmin(LeafletGeoAdmin):
    fields = ('title', 'points', 'object')

class LinesAdmin(LeafletGeoAdmin):
    fields = ('title', 'lines', 'object')

class PolygonsAdmin(LeafletGeoAdmin):
    fields = ('title', 'polygons', 'object')

admin.site.register(Points, PointsAdmin)
admin.site.register(Lines, LinesAdmin)
admin.site.register(Polygons, PolygonsAdmin)

admin.site.register(Xabarlar)
admin.site.register(Worker)
admin.site.register(Object)
admin.site.register(Branch)
admin.site.register(Department)
admin.site.register(PdoWork)
admin.site.register(ProgramWorkForm)
admin.site.register(ProgramWork)
admin.site.register(ProgramWorkFiles)
admin.site.register(Order)
admin.site.register(AktKomeralForm)
admin.site.register(KameralWorkReject)
admin.site.register(LeaderKomeralWorkReject)

admin.site.register(AktPolevoyForm)
admin.site.register(WorkerObject)
admin.site.register(History)
admin.site.register(ProgramWorkFormTable1)
admin.site.register(ProgramWorkFormTable2)
admin.site.register(ProgramWorkReject)
admin.site.register(Report)

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

admin.site.register(Period)
admin.site.register(WorkType)



