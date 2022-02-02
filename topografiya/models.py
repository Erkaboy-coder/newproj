from django.db import models
from django.conf import settings
from datetime import datetime, date, timezone
User = settings.AUTH_USER_MODEL
# Create your models here.
from django.core.serializers import serialize

class Department(models.Model):
    name = models.CharField(max_length=250, blank=True)
    leader = models.CharField(max_length=250, blank=True)
    tel_number = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    def __str__(self):
        return self.name

class BaseModel(models.Model):
    def save(self, *args, full_clean=True, **kwargs):
        if full_clean:
            self.full_clean()
            super().save(*args, **kwargs)

    class Meta(object):
        abstract = True

class Branch(models.Model):
    name = models.CharField(max_length=250, blank=True)
    leader = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Branches"

    # def natural_key(self):
    #     return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

class Worker(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.PROTECT,
        verbose_name="Related user",
        help_text="User linked to this profile")
    full_name = models.CharField(verbose_name="fullname", max_length=256)
    permission = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email', default='', max_length=250, blank=True)
    contact = models.CharField(verbose_name='contact', default='', max_length=250, blank=True)
    department = models. ForeignKey(Department, blank=True, on_delete=models.CASCADE, related_name='departments')
    position = models.CharField(verbose_name='position', default='', max_length=250, blank=True)
    branch = models.ForeignKey(Branch, blank=True, on_delete=models.CASCADE, related_name='workerbranch')
    status_worker = (
        ('0', 'Ishchi'),
        ('1', 'Bo\'lim boshlig\'i'),
        ('2', 'Geodezis'),
        ('2', 'Ogogd'),
    )
    status = models.CharField(verbose_name='Ishchi', default='0', max_length=10, choices=status_worker)

    live_admin = (
        ('0', 'Faol emas'),
        ('1', 'Faol'),
    )
    live = models.CharField(verbose_name='faol', default='0', max_length=10, choices=live_admin)

    class Meta(object):
        verbose_name = "Worker"
        verbose_name_plural = "Workers"
    def __str__(self):
        return self.user.username


class PdoWork(models.Model):
    agreement_date = models.CharField(verbose_name='Agreement date', max_length=250)
    object_name = models.CharField(verbose_name='Object name', max_length=250, blank=True)
    object_number = models.CharField(verbose_name='Object number', max_length=250, blank=True)
    object_address = models.CharField(verbose_name='Object address', max_length=250, blank=True)
    work_type = models.CharField(verbose_name='Work type', max_length=250, blank=True)
    work_term = models.CharField(verbose_name='work term', max_length=250, blank=True)
    department = models.CharField(verbose_name='Department', max_length=250, blank=True)
    object_cost = models.CharField(verbose_name='Object costs', max_length=250, blank=True)
    customer = models.CharField(verbose_name='Customer', max_length=250, blank=True)
    customer_info = models.CharField(verbose_name='Customer info', max_length=250, blank=True)
    branch = models.ForeignKey(Branch, blank=True, on_delete=models.CASCADE, related_name='branch')
    status = models.IntegerField(default=0, blank=True)
    status_recive = models.IntegerField(default=0, blank=True)
    # status_recive=0 yangi qabul qilingan ishlar
    # status_recive=1 bu ish qabul qilmagan ishlar
    # status_recive=2 ishchi qabul qilgan ishlar
    latter = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/latter', blank=True)
    tz = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/tz', blank=True)
    smeta = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/smeta', blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.work_type

    class Meta:
        verbose_name_plural = "PdoWorks"

    def natural_key(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields if f.name!='branch' and f.name!='latter' and f.name!='tz' and f.name!='smeta']])

class Object(models.Model):
    pdowork = models.ForeignKey(PdoWork, blank=True, on_delete=models.CASCADE, related_name='pdoworkobject')
    worker_leader = models.CharField(verbose_name='Worker leader', max_length=250,blank=True,)
    worker_ispolnitel = models.CharField(verbose_name='Worker ispolnitel', max_length=250,blank=True,)
    worker_geodezis = models.CharField(verbose_name='Worker geodezis', max_length=250,blank=True,)
    worker_ogogd = models.CharField(verbose_name='Worker ogogd', max_length=250,blank=True,)
    # status_report_work = models.IntegerField(default=0)
    isset_programwork = models.BooleanField(default=False)

    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.pdowork.object_name

    class Meta:
        verbose_name_plural = "Object"

    # def natural_key(self):
    #     return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
class ProgramWork(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='programworkforobject')
    status = models.IntegerField(default=0)
    # status  = 0 bu yangi kelib tushgan
    # status  = 1 bu tekshiruvga yuborilgan
    # status  = 2 bu qaytarilgan ish
    # status  = 4 bu tasdiqlangan
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.object.pdowork.object_name

    class Meta:
        verbose_name_plural = "ProgramWork"

class ProgramWorkReject(models.Model):
    programowork = models.ForeignKey(ProgramWork, blank=True, on_delete=models.CASCADE, related_name='programworkreject')
    file = models.FileField("Qaytarilgan fayl", upload_to='topografiya/static/files/programfiles', blank=True)
    reason = models.TextField(blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.programowork.object.pdowork.object_name

    class Meta:
        verbose_name_plural = "ProgramWorkReject"

class ProgramWorkForm(models.Model):
    programwork = models.ForeignKey(ProgramWork, blank=True, on_delete=models.CASCADE, related_name='programwork')
    file = models.FileField("Pogramma ish fayli", upload_to='topografiya/static/files/programfiles', blank=True)

    a0 = models.TextField(blank=True)
    a1_1 = models.TextField(blank=True)
    a1_2 = models.TextField(blank=True)
    a1_3 = models.TextField(blank=True)
    a2 = models.TextField(blank=True)
    a3 = models.TextField(blank=True)
    a4 = models.TextField(blank=True)
    a5 = models.TextField(blank=True)
    a6 = models.TextField(blank=True)
    a7 = models.TextField(blank=True)

    a7_2 = models.TextField(blank=True)
    a7_3 = models.TextField(blank=True)
    a7_4 = models.TextField(blank=True)

    a8 = models.TextField(blank=True)
    a8_1 = models.TextField(blank=True)
    a9_1 = models.TextField(blank=True)
    # jadval
    a9_3 = models.TextField(blank=True)
    a9_4 = models.TextField(blank=True)

    a10 = models.TextField(blank=True)
    a11 = models.TextField(blank=True)
    a12 = models.TextField(blank=True)
    program_work_creator = models.TextField(blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.a0

    class Meta:
        verbose_name_plural = "ProgramWorkForm"

class ProgramWorkFormTable1(models.Model):
    programworkform = models.ForeignKey(ProgramWorkForm, blank=True, on_delete=models.CASCADE, related_name='programworkform')
    a7_1_1 = models.TextField(blank=True)
    a7_1_2 = models.TextField(blank=True)
    a7_1_3 = models.TextField(blank=True)
    a7_1_4 = models.TextField(blank=True)
    a7_1_5 = models.TextField(blank=True)

    def __str__(self):
        return self.a7_1_1

    class Meta:
        verbose_name_plural = "ProgramWorkFormTable1"

class ProgramWorkFormTable2(models.Model):
    programworkform = models.ForeignKey(ProgramWorkForm, blank=True, on_delete=models.CASCADE, related_name='programworkform2')

    a9_2_1 = models.TextField(blank=True)
    a9_2_2 = models.TextField(blank=True)
    a9_2_3 = models.TextField(blank=True)
    a9_2_4 = models.TextField(blank=True)
    a9_2_5 = models.TextField(blank=True)
    a9_2_6 = models.TextField(blank=True)
    a9_2_7 = models.TextField(blank=True)

    def __str__(self):
        return self.a9_2_1

    class Meta:
        verbose_name_plural = "ProgramWorkFormTable2"



class AktKomeralForm(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='aktkomeralobject')
    status_komeral_work = models.IntegerField(default=0)

    status = models.IntegerField(default=0)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "AktKomeralForm"

class AktPolevoyForm(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='sktpolevoyobject')
    status_polevoy_work = models.IntegerField(default=0)

    status = models.IntegerField(default=0)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "AktPolevoyForm"

class WorkerObject(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='workerobject')
    abris_file = models.FileField("Abris hujjat fayli", upload_to='topografiya/static/files/abrisfiles', blank=True)
    kroki_file = models.FileField("Kroki hujjat fayli", upload_to='topografiya/static/files/krokifiles', blank=True)
    jurnal_file = models.FileField("Jurnal hujjat fayli", upload_to='topografiya/static/files/jurnalfiles', blank=True)
    vidimes_file = models.FileField("Vidimes hujjat fayli", upload_to='topografiya/static/files/vidimes', blank=True)
    list_agreement_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/agreementfiles', blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.object.pdowork.object_name

    class Meta:
        verbose_name_plural = "WorkerObjects"


class SirieFiles(models.Model):
    workerobject = models.ForeignKey(WorkerObject, blank=True, on_delete=models.CASCADE, related_name='workerobjectsiriefiles')
    file1_1 = models.FileField("Hujjat fayli bpla1", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_2 = models.FileField("Hujjat fayli bpla2", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_3 = models.FileField("Hujjat fayli bpla3", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_4 = models.FileField("Hujjat fayli bpla4", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_5 = models.FileField("Hujjat fayli bpla5", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_6 = models.FileField("Hujjat fayli bpla6", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_7 = models.FileField("Hujjat fayli bpla7", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_8 = models.FileField("Hujjat fayli bpla8", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_9 = models.FileField("Hujjat fayli bpla9", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_10 = models.FileField("Hujjat fayli bpla10", upload_to='topografiya/static/files/siriefiles',blank=True)
    file1_11 = models.FileField("Hujjat fayli bpla11", upload_to='topografiya/static/files/siriefiles',blank=True)

    file2_1 = models.FileField("Hujjat fayli bpla2_1", upload_to='topografiya/static/files/siriefiles', blank=True)
    file2_2 = models.FileField("Hujjat fayli bpla2_2", upload_to='topografiya/static/files/siriefiles', blank=True)
    file2_3 = models.FileField("Hujjat fayli bpla2_3", upload_to='topografiya/static/files/siriefiles', blank=True)
    file2_4 = models.FileField("Hujjat fayli bpla2_4", upload_to='topografiya/static/files/siriefiles', blank=True)
    file2_5 = models.FileField("Hujjat fayli bpla2_5", upload_to='topografiya/static/files/siriefiles', blank=True)
    file2_6 = models.FileField("Hujjat fayli bpla2_6", upload_to='topografiya/static/files/siriefiles', blank=True)
    file2_7 = models.FileField("Hujjat fayli bpla2_7", upload_to='topografiya/static/files/siriefiles', blank=True)

    file3_1 = models.FileField("Hujjat fayli bpla3_1", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_2 = models.FileField("Hujjat fayli bpla3_2", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_3 = models.FileField("Hujjat fayli bpla3_3", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_4 = models.FileField("Hujjat fayli bpla3_4", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_5 = models.FileField("Hujjat fayli bpla3_5", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_6 = models.FileField("Hujjat fayli bpla3_6", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_7 = models.FileField("Hujjat fayli bpla3_7", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_8 = models.FileField("Hujjat fayli bpla3_8", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_9 = models.FileField("Hujjat fayli bpla3_9", upload_to='topografiya/static/files/siriefiles', blank=True)
    file3_10 = models.FileField("Hujjat fayli bpla3_10", upload_to='topografiya/static/files/siriefiles', blank=True)
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.workerobject.object.pdowork.object_name

    class Meta:
        verbose_name_plural = "SirieFiles"

class PoyasitelniyForm(models.Model):
    workerobject = models.ForeignKey(WorkerObject, blank=True, on_delete=models.CASCADE, related_name='workerobjectpoyasitelniy')
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.info

    class Meta:
        verbose_name_plural = "PoyasitelniyForm"

class TopografikPlan(models.Model):
    workerobject = models.ForeignKey(WorkerObject, blank=True, on_delete=models.CASCADE, related_name='workerobjecttopografikplan')
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.info
    class Meta:
        verbose_name_plural = "TopografikPlan"

class Order(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='orderobject')

    info = models.TextField(blank=True)
    method_creation = models.TextField(blank=True)
    method_fill = models.TextField(blank=True)
    syomka = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    item_check = models.TextField(blank=True)

    adjustment_methods= models.TextField(blank=True)
    list_of_materials = models.TextField(blank=True)

    order_creator = models.TextField(blank=True)
    order_receiver = models.TextField(blank=True)

    type_order = (
        ('0', 'БПЛА'),
        ('1', 'GNSS'),
        ('2', 'Тахеометрическая съемка'),
    )
    type_of_sirie = models.CharField(verbose_name='type_of_work', default='1', max_length=10, choices=type_order)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.info

    class Meta:
        verbose_name_plural = "Order"
class History(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='historyobject')
    status = models.IntegerField(default=0)
    # status=4 bolsa bu program rabotni tasdiqlagan bo'ladi
    # status=5 bolsa bu program rabotni rad etilgan
    # status=6 bolsa bu program rabotni qayta tekshiruvga yuborildi
    # status = 7, Dala nazoratiga sirie ma'lumotlari yuklandi
    user_id = models.CharField(verbose_name='user', max_length=250,blank=True)
    file = models.FileField("Tarix fayli", upload_to='topografiya/static/files/history', blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    comment = models.TextField(blank=True)
    def __str__(self):
        return self.object.pdowork.object_name
    class Meta:
        verbose_name_plural = "History"