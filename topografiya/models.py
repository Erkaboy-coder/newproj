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

class AktPolevoyForm(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='aktpolevoyobject')
    status = models.IntegerField(default=0)

    a1 = models.TextField(blank=True)
    a2 = models.TextField(blank=True)
    a3 = models.TextField(blank=True)
    a4 = models.TextField(blank=True)
    a5 = models.TextField(blank=True)
    a6 = models.TextField(blank=True)
    a7 = models.TextField(blank=True)
    a8 = models.TextField(blank=True)
    a9 = models.TextField(blank=True)
    a10 = models.TextField(blank=True)
    a11 = models.TextField(blank=True)
    a12 = models.TextField(blank=True)
    a13 = models.TextField(blank=True)
    a14 = models.TextField(blank=True)
    a15 = models.TextField(blank=True)
    a16 = models.TextField(blank=True)
    a17 = models.TextField(blank=True)
    a18 = models.TextField(blank=True)
    a19 = models.TextField(blank=True)
    a20 = models.TextField(blank=True)
    a21 = models.TextField(blank=True)
    a22 = models.TextField(blank=True)
    a23 = models.TextField(blank=True)
    a24 = models.TextField(blank=True)
    a25 = models.TextField(blank=True)
    a26 = models.TextField(blank=True)
    a27 = models.TextField(blank=True)
    a28 = models.TextField(blank=True)
    a29 = models.TextField(blank=True)
    a30 = models.TextField(blank=True)
    a31 = models.TextField(blank=True)
    a32 = models.TextField(blank=True)
    a33 = models.TextField(blank=True)
    a34 = models.TextField(blank=True)
    a35 = models.TextField(blank=True)
    a36 = models.TextField(blank=True)
    a37 = models.TextField(blank=True)
    a38 = models.TextField(blank=True)
    a39 = models.TextField(blank=True)
    a40 = models.TextField(blank=True)
    a41 = models.TextField(blank=True)
    a42 = models.TextField(blank=True)
    a43 = models.TextField(blank=True)
    a44 = models.TextField(blank=True)
    a45 = models.TextField(blank=True)
    a46 = models.TextField(blank=True)
    a47 = models.TextField(blank=True)
    a48 = models.TextField(blank=True)
    a49 = models.TextField(blank=True)
    a50 = models.TextField(blank=True)
    a51 = models.TextField(blank=True)
    a52 = models.TextField(blank=True)
    a53 = models.TextField(blank=True)
    a54 = models.TextField(blank=True)
    a55 = models.TextField(blank=True)
    a56 = models.TextField(blank=True)
    a57 = models.TextField(blank=True)
    a58 = models.TextField(blank=True)
    a59 = models.TextField(blank=True)
    a60 = models.TextField(blank=True)
    a61 = models.TextField(blank=True)
    a62 = models.TextField(blank=True)
    a63 = models.TextField(blank=True)
    a64 = models.TextField(blank=True)
    a65 = models.TextField(blank=True)
    a66 = models.TextField(blank=True)
    a67 = models.TextField(blank=True)
    a68 = models.TextField(blank=True)
    a69 = models.TextField(blank=True)
    a70 = models.TextField(blank=True)
    a71 = models.TextField(blank=True)
    a72 = models.TextField(blank=True)
    a73 = models.TextField(blank=True)
    a74 = models.TextField(blank=True)
    a75 = models.TextField(blank=True)
    a76 = models.TextField(blank=True)
    a77 = models.TextField(blank=True)
    a78 = models.TextField(blank=True)
    a79 = models.TextField(blank=True)
    a80 = models.TextField(blank=True)
    a81 = models.TextField(blank=True)
    a82 = models.TextField(blank=True)
    a83 = models.TextField(blank=True)
    a84 = models.TextField(blank=True)
    a85 = models.TextField(blank=True)
    a86 = models.TextField(blank=True)
    a87 = models.TextField(blank=True)
    a88 = models.TextField(blank=True)
    a89 = models.TextField(blank=True)
    a90 = models.TextField(blank=True)
    a91 = models.TextField(blank=True)
    a92 = models.TextField(blank=True)
    a93 = models.TextField(blank=True)
    a94 = models.TextField(blank=True)
    a95 = models.TextField(blank=True)
    a96 = models.TextField(blank=True)
    a97 = models.TextField(blank=True)
    a98 = models.TextField(blank=True)
    a99 = models.TextField(blank=True)
    a100 = models.TextField(blank=True)
    a101 = models.TextField(blank=True)
    a102 = models.TextField(blank=True)
    a103 = models.TextField(blank=True)
    a104 = models.TextField(blank=True)
    a105 = models.TextField(blank=True)
    a106 = models.TextField(blank=True)
    a107 = models.TextField(blank=True)
    a108 = models.TextField(blank=True)
    a109 = models.TextField(blank=True)
    a110 = models.TextField(blank=True)
    a111 = models.TextField(blank=True)
    a112 = models.TextField(blank=True)
    a113 = models.TextField(blank=True)
    a114 = models.TextField(blank=True)
    a115 = models.TextField(blank=True)
    a116 = models.TextField(blank=True)
    a117 = models.TextField(blank=True)
    a118 = models.TextField(blank=True)
    a119 = models.TextField(blank=True)
    a120 = models.TextField(blank=True)
    a121 = models.TextField(blank=True)
    a122 = models.TextField(blank=True)
    a123 = models.TextField(blank=True)
    a124 = models.TextField(blank=True)
    a125 = models.TextField(blank=True)
    a126 = models.TextField(blank=True)

    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.a2

    class Meta:
        verbose_name_plural = "AktPolevoyForm"

class AktPolovoyTable1(models.Model):
    aktpolovoy = models.ForeignKey(AktPolevoyForm, blank=True, on_delete=models.CASCADE, related_name='aktpolovoytable1')

    a1_1 = models.TextField(blank=True)
    a1_2 = models.TextField(blank=True)
    a1_3 = models.TextField(blank=True)
    a1_4 = models.TextField(blank=True)
    a1_5 = models.TextField(blank=True)
    a1_6 = models.TextField(blank=True)
    a1_7 = models.TextField(blank=True)

    def __str__(self):
        return self.a1_1

    class Meta:
        verbose_name_plural = "AktPolovoyTable1"

class AktPolovoyTable2(models.Model):
    aktpolovoy = models.ForeignKey(AktPolevoyForm, blank=True, on_delete=models.CASCADE, related_name='aktpolovoytable2')

    a2_1 = models.TextField(blank=True)
    a2_2 = models.TextField(blank=True)
    a2_3 = models.TextField(blank=True)
    a2_4 = models.TextField(blank=True)
    a2_5 = models.TextField(blank=True)
    a2_6 = models.TextField(blank=True)
    a2_7 = models.TextField(blank=True)

    def __str__(self):
        return self.a2_1

    class Meta:
        verbose_name_plural = "AktPolovoyTable2"

class AktPolovoyTable3(models.Model):
    aktpolovoy = models.ForeignKey(AktPolevoyForm, blank=True, on_delete=models.CASCADE, related_name='aktpolovoytable3')

    a3_1 = models.TextField(blank=True)
    a3_2 = models.TextField(blank=True)
    a3_3 = models.TextField(blank=True)
    a3_4 = models.TextField(blank=True)
    a3_5 = models.TextField(blank=True)
    a3_6 = models.TextField(blank=True)
    a3_7 = models.TextField(blank=True)
    a3_8 = models.TextField(blank=True)
    a3_9 = models.TextField(blank=True)

    def __str__(self):
        return self.a3_1

    class Meta:
        verbose_name_plural = "AktPolovoyTable3"

class AktPolovoyTable4(models.Model):
    aktpolovoy = models.ForeignKey(AktPolevoyForm, blank=True, on_delete=models.CASCADE, related_name='aktpolovoytable4')

    a4_1 = models.TextField(blank=True)
    a4_2 = models.TextField(blank=True)
    a4_3 = models.TextField(blank=True)
    a4_4 = models.TextField(blank=True)
    a4_5 = models.TextField(blank=True)
    a4_6 = models.TextField(blank=True)

    def __str__(self):
        return self.a4_1

    class Meta:
        verbose_name_plural = "AktPolovoyTable4"

class AktPolovoyTable5(models.Model):
    aktpolovoy = models.ForeignKey(AktPolevoyForm, blank=True, on_delete=models.CASCADE, related_name='aktpolovoytable5')

    a5_1 = models.TextField(blank=True)
    a5_2 = models.TextField(blank=True)
    a5_3 = models.TextField(blank=True)
    a5_4 = models.TextField(blank=True)
    a5_5 = models.TextField(blank=True)
    a5_6 = models.TextField(blank=True)

    def __str__(self):
        return self.a5_1

    class Meta:
        verbose_name_plural = "AktPolovoyTable5"

class AktPolovoyTable6(models.Model):
    aktpolovoy = models.ForeignKey(AktPolevoyForm, blank=True, on_delete=models.CASCADE, related_name='aktpolovoytable6')

    a6_1 = models.TextField(blank=True)
    a6_2 = models.TextField(blank=True)
    a6_3 = models.TextField(blank=True)
    a6_4 = models.TextField(blank=True)
    a6_5 = models.TextField(blank=True)
    a6_6 = models.TextField(blank=True)
    a6_7 = models.TextField(blank=True)
    a6_8 = models.TextField(blank=True)
    a6_9 = models.TextField(blank=True)

    def __str__(self):
        return self.a6_1

    class Meta:
        verbose_name_plural = "AktPolovoyTable6"

class AktPolovoyTable7(models.Model):
    aktpolovoy = models.ForeignKey(AktPolevoyForm, blank=True, on_delete=models.CASCADE, related_name='aktpolovoytable7')

    a7_1 = models.TextField(blank=True)
    a7_2 = models.TextField(blank=True)
    a7_3 = models.TextField(blank=True)
    a7_4 = models.TextField(blank=True)
    a7_5 = models.TextField(blank=True)

    def __str__(self):
        return self.a7_1

    class Meta:
        verbose_name_plural = "AktPolovoyTable7"

class AktPolovoyTable8(models.Model):
    aktpolovoy = models.ForeignKey(AktPolevoyForm, blank=True, on_delete=models.CASCADE, related_name='aktpolovoytable8')

    a8_1 = models.TextField(blank=True)
    a8_2 = models.TextField(blank=True)
    a8_3 = models.TextField(blank=True)
    a8_4 = models.TextField(blank=True)
    a8_5 = models.TextField(blank=True)

    def __str__(self):
        return self.a8_1

    class Meta:
        verbose_name_plural = "AktPolovoyTable8"


class WorkerObject(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='workerobject')
    abris_file = models.FileField("Abris hujjat fayli", upload_to='topografiya/static/files/abrisfiles', blank=True)
    kroki_file = models.FileField("Kroki hujjat fayli", upload_to='topografiya/static/files/krokifiles', blank=True)
    jurnal_file = models.FileField("Jurnal hujjat fayli", upload_to='topografiya/static/files/jurnalfiles', blank=True)
    vidimes_file = models.FileField("Vidimes hujjat fayli", upload_to='topografiya/static/files/vidimes', blank=True)
    list_agreement_file = models.FileField("Hujjat fayli", upload_to='topografiya/static/files/agreementfiles', blank=True)
    status = models.IntegerField(default=0)
    # status = 0 bolsa yangi
    # status = 1 tekshiruvga kelgan
    # status = 2 qaytarilgan
    # status = 3 muddati kam qolgan
    # status = 4 tasdiqlangan
    status_geodezis_komeral = models.IntegerField(default=0)
    # status = 1 glavniy geodezisga yuborilgan tekshirish uchun
    # status = 2 qaytarilgan
    # status = 3 muddati kam qolgan
    # status = 4 tasdiqlangan
    def __str__(self):
        return self.object.pdowork.object_name

    class Meta:
        verbose_name_plural = "WorkerObjects"

class PolevoyWorkReject(models.Model):
    workerobject = models.ForeignKey(WorkerObject, blank=True, on_delete=models.CASCADE, related_name='polevoymworkreject')
    file = models.FileField("Qaytarilgan fayl", upload_to='topografiya/static/files/polevoy_rejects', blank=True)
    reason = models.TextField(blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.workerobject.object.pdowork.object_name

    class Meta:
        verbose_name_plural = "PolevoyWorkReject"

class KameralWorkReject(models.Model):
    workerobject = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='komeralworkreject')
    file = models.FileField("Qaytarilgan fayl", upload_to='topografiya/static/files/kameral_rejects', blank=True)
    reason = models.TextField(blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.workerobject.pdowork.object_name

    class Meta:
        verbose_name_plural = "KomeralWorkReject"

class LeaderKomeralWorkReject(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='leaderkomeralworkreject')
    file = models.FileField("Qaytarilgan fayl", upload_to='topografiya/static/files/programfiles', blank=True)
    reason = models.TextField(blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.object.pdowork.object_name

    class Meta:
        verbose_name_plural = "LeaderKomeralWorkReject"

class AktKomeralForm(models.Model):
    object = models.ForeignKey(Object, blank=True, on_delete=models.CASCADE, related_name='aktkomeralobject')
    status = models.IntegerField(default=0)
    # status = 0 bosa komeral tekshiruvga kelgan ish
    # status = 1 bosa komeral nazorati tekshiruvida
    # status = 2 bosa komeral nazoratdan qaytgan ish
    # status = 3 muddati kam qolgan
    # status = 4 tasdiqlanganlar

    a1 = models.TextField(blank=True)
    a2 = models.TextField(blank=True)
    a3 = models.TextField(blank=True)
    a4 = models.TextField(blank=True)
    a5 = models.TextField(blank=True)
    a6 = models.TextField(blank=True)
    a7 = models.TextField(blank=True)
    a8 = models.TextField(blank=True)
    a9 = models.TextField(blank=True)
    a10 = models.TextField(blank=True)
    a11 = models.TextField(blank=True)
    a12 = models.TextField(blank=True)
    a13 = models.TextField(blank=True)
    a14 = models.TextField(blank=True)
    a15 = models.TextField(blank=True)
    a16 = models.TextField(blank=True)
    a17 = models.TextField(blank=True)
    a18 = models.TextField(blank=True)
    a19 = models.TextField(blank=True)
    a20 = models.TextField(blank=True)
    a21 = models.TextField(blank=True)
    a22 = models.TextField(blank=True)
    a23 = models.TextField(blank=True)
    a24 = models.TextField(blank=True)
    a25 = models.TextField(blank=True)
    a26 = models.TextField(blank=True)
    a27 = models.TextField(blank=True)
    a28 = models.TextField(blank=True)
    a29 = models.TextField(blank=True)
    a30 = models.TextField(blank=True)
    a31 = models.TextField(blank=True)
    a32 = models.TextField(blank=True)
    a33 = models.TextField(blank=True)
    a34 = models.TextField(blank=True)
    a35 = models.TextField(blank=True)
    a36 = models.TextField(blank=True)
    a37 = models.TextField(blank=True)
    a38 = models.TextField(blank=True)
    a39 = models.TextField(blank=True)
    a40 = models.TextField(blank=True)
    a41 = models.TextField(blank=True)
    a42 = models.TextField(blank=True)
    a43 = models.TextField(blank=True)
    a44 = models.TextField(blank=True)
    a45 = models.TextField(blank=True)
    a46 = models.TextField(blank=True)
    a47 = models.TextField(blank=True)
    a48 = models.TextField(blank=True)
    a49 = models.TextField(blank=True)
    a50 = models.TextField(blank=True)
    a51 = models.TextField(blank=True)
    a52 = models.TextField(blank=True)
    a53 = models.TextField(blank=True)
    a54 = models.TextField(blank=True)
    a55 = models.TextField(blank=True)
    a56 = models.TextField(blank=True)
    a57 = models.TextField(blank=True)
    a58 = models.TextField(blank=True)
    a59 = models.TextField(blank=True)
    a60 = models.TextField(blank=True)
    a61 = models.TextField(blank=True)
    a62 = models.TextField(blank=True)
    a63 = models.TextField(blank=True)
    a64 = models.TextField(blank=True)

    def __str__(self):
        return self.object.pdowork.object_name

    class Meta:
        verbose_name_plural = "AktKomeralForm"



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

    b1 = models.TextField(blank=True)
    b2 = models.TextField(blank=True)
    b_1 = models.TextField(blank=True)
    b_2 = models.TextField(blank=True)
    b3 = models.TextField(blank=True)
    b3_1 = models.TextField(blank=True)
    b4 = models.TextField(blank=True)
    b5 = models.TextField(blank=True)
    b6 = models.TextField(blank=True)
    b7 = models.TextField(blank=True)
    # jadval
    b8_1_1 = models.TextField(blank=True)
    # jadval
    b10 = models.TextField(blank=True)
    b11 = models.TextField(blank=True)
    b12 = models.TextField(blank=True)
    b13 = models.TextField(blank=True)
    b14 = models.TextField(blank=True)
    b15 = models.TextField(blank=True)
    b16_a = models.TextField(blank=True)
    b16_b = models.TextField(blank=True)
    # jadval
    # jadval
    b19 = models.TextField(blank=True)
    b19_1 = models.TextField(blank=True)
    b19_2 = models.TextField(blank=True)
    b20 = models.TextField(blank=True)
    b21 = models.TextField(blank=True)
    # table
    c_1 = models.TextField(blank=True)
    c_2 = models.TextField(blank=True)
    c_3 = models.TextField(blank=True)
    c_4 = models.TextField(blank=True)
    c_5 = models.TextField(blank=True)
    c_6 = models.TextField(blank=True)
    c_7 = models.TextField(blank=True)
    c_8 = models.TextField(blank=True)
    c_9 = models.TextField(blank=True)
    c_10 = models.TextField(blank=True)
    c_11 = models.TextField(blank=True)
    c_12 = models.TextField(blank=True)
    c_13 = models.TextField(blank=True)
    c_14 = models.TextField(blank=True)
    c_15 = models.TextField(blank=True)
    c_16 = models.TextField(blank=True)
    c_17 = models.TextField(blank=True)
    c_18 = models.TextField(blank=True)
    c_19 = models.TextField(blank=True)
    c_20 = models.TextField(blank=True)
    c_21 = models.TextField(blank=True)
    c_22 = models.TextField(blank=True)
    c_23 = models.TextField(blank=True)
    c_24 = models.TextField(blank=True)
    c_25 = models.TextField(blank=True)
    c_26 = models.TextField(blank=True)

    d_1 = models.TextField(blank=True)
    d_2 = models.TextField(blank=True)
    d_3 = models.TextField(blank=True)
    d_4 = models.TextField(blank=True)
    d_5 = models.TextField(blank=True)
    d_6 = models.TextField(blank=True)
    d_7 = models.TextField(blank=True)
    d_8 = models.TextField(blank=True)
    d_9 = models.TextField(blank=True)
    d_10 = models.TextField(blank=True)
    d_11 = models.TextField(blank=True)
    d_12 = models.TextField(blank=True)
    d_13 = models.TextField(blank=True)

    info = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.b1

    class Meta:
        verbose_name_plural = "PoyasitelniyForm"

class PoyasitelniyFormTable1(models.Model):
    poyasitelniyform = models.ForeignKey(PoyasitelniyForm, blank=True, on_delete=models.CASCADE, related_name='workerobjectpoyasitelniyformtable1')

    b8_1 = models.TextField(blank=True)
    b8_2 = models.TextField(blank=True)
    b8_3 = models.TextField(blank=True)
    b8_4 = models.TextField(blank=True)
    # jadval
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.b8_1

    class Meta:
        verbose_name_plural = "PoyasitelniyFormTable1"

class PoyasitelniyFormTable2(models.Model):
    poyasitelniyform = models.ForeignKey(PoyasitelniyForm, blank=True, on_delete=models.CASCADE, related_name='workerobjectpoyasitelniyformtable2')

    b9_1 = models.TextField(blank=True)
    b9_2 = models.TextField(blank=True)
    b9_3 = models.TextField(blank=True)
    b9_4 = models.TextField(blank=True)
    # jadval
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.b9_1

    class Meta:
        verbose_name_plural = "PoyasitelniyFormTable2"

class PoyasitelniyFormTable3(models.Model):
    poyasitelniyform = models.ForeignKey(PoyasitelniyForm, blank=True, on_delete=models.CASCADE, related_name='workerobjectpoyasitelniyformtable3')

    b17_1 = models.TextField(blank=True)
    b17_2 = models.TextField(blank=True)
    b17_3 = models.TextField(blank=True)
    b17_4 = models.TextField(blank=True)
    b17_5 = models.TextField(blank=True)
    b17_6 = models.TextField(blank=True)
    b17_7 = models.TextField(blank=True)
    # jadval
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.b17_1

    class Meta:
        verbose_name_plural = "PoyasitelniyFormTable3"

class PoyasitelniyFormTable4(models.Model):
    poyasitelniyform = models.ForeignKey(PoyasitelniyForm, blank=True, on_delete=models.CASCADE, related_name='workerobjectpoyasitelniyformtable4')
    b18_1 = models.TextField(blank=True)
    b18_2 = models.TextField(blank=True)
    b18_3 = models.TextField(blank=True)
    b18_4 = models.TextField(blank=True)
    b18_5 = models.TextField(blank=True)
    # jadval
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.b18_1

    class Meta:
        verbose_name_plural = "PoyasitelniyFormTable4"

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
    # status = 4 bolsa bu program rabotni tasdiqlagan bo'ladi
    # status = 5 bolsa bu program rabotni rad etilgan
    # status = 6 bolsa bu program rabotni qayta tekshiruvga yuborildi
    # status = 7 Dala nazoratiga sirie ma'lumotlari yuklandi
    # status = 8 Dala nazoratiga fayl yuklandi
    # status = 9 Dala nazoratiga poyasitelniy formaga ma'lumot yuklandi
    # status = 10 Dala nazorati tekshiruviga yuborilgan ish
    # status = 11 Dala nazorati tekshiruvi akt yaratildi
    # status = 12 Dala nazorati tekshiruvi akt o'zgartirildi
    # status = 13 Dala nazorati tekshiruvi tasdqilandi
    # status = 14 Dala nazorati tekshiruvi rad etildi
    # status = 15 komeral nazorati rad etildi
    # status = 16 komeral nazoratga teskhiruviga qayta yuborildi
    # status = 17 komeral nazoratidan o'tgan ish
    # status = 18 Geodezis komeral nazoratidan qaytarilgan ish
    # status = 19 Geodezis komeral nazoratidan qayta yuborilgan ish
    user_id = models.CharField(verbose_name='user', max_length=250,blank=True)
    file = models.FileField("Tarix fayli", upload_to='topografiya/static/files/history', blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    comment = models.TextField(blank=True)
    def __str__(self):
        return self.object.pdowork.object_name
    class Meta:
        verbose_name_plural = "History"