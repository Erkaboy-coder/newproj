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
    worker_leader = models.CharField(verbose_name='Worker leader', max_length=250)
    worker_ispolnitel = models.CharField(verbose_name='Worker ispolnitel', max_length=250)
    worker_geodezis = models.CharField(verbose_name='Worker geodezis', max_length=250)
    worker_ogogd = models.CharField(verbose_name='Worker ogogd', max_length=250)
    # status_report_work = models.IntegerField(default=0)
    isset_programwork = models.BooleanField(default=False)

    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.pdowork.object_name

    class Meta:
        verbose_name_plural = "Object"

    # def natural_key(self):
    #     return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

class ProgramWorkForm(models.Model):
    status = models.IntegerField(default=0)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "ProgramWorkForm"

class ProgramWork(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='programworkforobject')
    status_program_work = models.IntegerField(default=0)

    agreement_date = models.CharField(verbose_name='Agreement date', max_length=250)
    file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/programfiles', blank=True)
    comment = models.TextField(blank=True)
    programworkform = models.ForeignKey(ProgramWorkForm, blank=True, on_delete=models.CASCADE, related_name='programworkform')
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.agreement_date

    class Meta:
        verbose_name_plural = "ProgramWork"

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
    raw_measurements_data_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/siriefiles', blank=True)
    abris_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/abrisfiles', blank=True)
    kroki_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/krokifiles', blank=True)
    jurnal_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/jurnalfiles', blank=True)
    list_agreement_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/agreementfiles', blank=True)
    poyasnitel_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/agreementfiles', blank=True)
    topografik_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/topografikfiles', blank=True)

    status = models.IntegerField(default=0)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "WorkerObjects"


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
    user_id = models.CharField(verbose_name='user', max_length=250,blank=True)
    file = models.FileField("Tarix fayli", upload_to='topografiya/static/files/history', blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "History"