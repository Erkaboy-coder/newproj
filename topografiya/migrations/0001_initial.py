# Generated by Django 4.0.1 on 2022-01-21 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('leader', models.CharField(blank=True, max_length=250)),
                ('address', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('leader', models.CharField(blank=True, max_length=250)),
                ('tel_number', models.CharField(blank=True, max_length=250)),
                ('email', models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_leader', models.CharField(max_length=250, verbose_name='Worker leader')),
                ('worker_ispolnitel', models.CharField(max_length=250, verbose_name='Worker ispolnitel')),
                ('worker_geodezis', models.CharField(max_length=250, verbose_name='Worker geodezis')),
                ('worker_ogogd', models.CharField(max_length=250, verbose_name='Worker ogogd')),
                ('isset_programwork', models.BooleanField(default=False)),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Object',
            },
        ),
        migrations.CreateModel(
            name='ProgramWorkForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'ProgramWorkForm',
            },
        ),
        migrations.CreateModel(
            name='WorkerObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_measurements_data_file', models.FileField(blank=True, upload_to='topografiya/static/files/siriefiles', verbose_name='Hujjat fayli')),
                ('abris_file', models.FileField(blank=True, upload_to='topografiya/static/files/abrisfiles', verbose_name='Hujjat fayli')),
                ('kroki_file', models.FileField(blank=True, upload_to='topografiya/static/files/krokifiles', verbose_name='Hujjat fayli')),
                ('jurnal_file', models.FileField(blank=True, upload_to='topografiya/static/files/jurnalfiles', verbose_name='Hujjat fayli')),
                ('list_agreement_file', models.FileField(blank=True, upload_to='topografiya/static/files/agreementfiles', verbose_name='Hujjat fayli')),
                ('poyasnitel_file', models.FileField(blank=True, upload_to='topografiya/static/files/agreementfiles', verbose_name='Hujjat fayli')),
                ('topografik_file', models.FileField(blank=True, upload_to='topografiya/static/files/topografikfiles', verbose_name='Hujjat fayli')),
                ('status', models.IntegerField(default=0)),
                ('object', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='workerobject', to='topografiya.object')),
            ],
            options={
                'verbose_name_plural': 'WorkerObjects',
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=256, verbose_name='fullname')),
                ('permission', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, default='', max_length=250, verbose_name='email')),
                ('contact', models.CharField(blank=True, default='', max_length=250, verbose_name='contact')),
                ('position', models.CharField(blank=True, default='', max_length=250, verbose_name='position')),
                ('status', models.CharField(choices=[('0', 'Ishchi'), ('1', "Bo'lim boshlig'i"), ('2', 'Geodezis'), ('2', 'Ogogd')], default='0', max_length=10, verbose_name='Ishchi')),
                ('live', models.CharField(choices=[('0', 'Faol emas'), ('1', 'Faol')], default='0', max_length=10, verbose_name='faol')),
                ('branch', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='workerbranch', to='topografiya.branch')),
                ('department', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='topografiya.department')),
                ('user', models.OneToOneField(help_text='User linked to this profile', on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Related user')),
            ],
            options={
                'verbose_name': 'Worker',
                'verbose_name_plural': 'Workers',
            },
        ),
        migrations.CreateModel(
            name='ProgramWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_program_work', models.IntegerField(default=0)),
                ('agreement_date', models.CharField(max_length=250, verbose_name='Agreement date')),
                ('file', models.FileField(blank=True, upload_to='topografiya/static/files/programfiles', verbose_name='Hujjat fayli')),
                ('comment', models.TextField(blank=True)),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
                ('object', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='programworkforobject', to='topografiya.object')),
                ('programworkform', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='programworkform', to='topografiya.programworkform')),
            ],
            options={
                'verbose_name_plural': 'ProgramWork',
            },
        ),
        migrations.CreateModel(
            name='PdoWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_date', models.CharField(max_length=250, verbose_name='Agreement date')),
                ('object_name', models.CharField(blank=True, max_length=250, verbose_name='Object name')),
                ('object_number', models.CharField(blank=True, max_length=250, verbose_name='Object number')),
                ('object_address', models.CharField(blank=True, max_length=250, verbose_name='Object address')),
                ('work_type', models.CharField(blank=True, max_length=250, verbose_name='Work type')),
                ('work_term', models.CharField(blank=True, max_length=250, verbose_name='work term')),
                ('department', models.CharField(blank=True, max_length=250, verbose_name='Department')),
                ('object_cost', models.CharField(blank=True, max_length=250, verbose_name='Object costs')),
                ('customer', models.CharField(blank=True, max_length=250, verbose_name='Customer')),
                ('customer_info', models.CharField(blank=True, max_length=250, verbose_name='Customer info')),
                ('status', models.IntegerField(blank=True, default=0)),
                ('status_recive', models.IntegerField(blank=True, default=0)),
                ('latter', models.FileField(blank=True, upload_to='topografiya/static/files/latter', verbose_name='Hujjat fayli')),
                ('tz', models.FileField(blank=True, upload_to='topografiya/static/files/tz', verbose_name='Hujjat fayli')),
                ('smeta', models.FileField(blank=True, upload_to='topografiya/static/files/smeta', verbose_name='Hujjat fayli')),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
                ('branch', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='branch', to='topografiya.branch')),
            ],
            options={
                'verbose_name_plural': 'PdoWorks',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True)),
                ('method_creation', models.TextField(blank=True)),
                ('method_fill', models.TextField(blank=True)),
                ('syomka', models.TextField(blank=True)),
                ('requirements', models.TextField(blank=True)),
                ('item_check', models.TextField(blank=True)),
                ('list_of_materials', models.TextField(blank=True)),
                ('adjustment_methods', models.TextField(blank=True)),
                ('order_creator', models.TextField(blank=True)),
                ('Order_receiver', models.TextField(blank=True)),
                ('type_of_sirie', models.CharField(choices=[('0', '????????'), ('1', 'GNSS'), ('2', '???????????????????????????????? ????????????')], default='1', max_length=10, verbose_name='type_of_work')),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
                ('object', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderobject', to='topografiya.object')),
            ],
            options={
                'verbose_name_plural': 'Order',
            },
        ),
        migrations.AddField(
            model_name='object',
            name='pdowork',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='pdoworkobject', to='topografiya.pdowork'),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('user_id', models.CharField(blank=True, max_length=250, verbose_name='user')),
                ('file', models.FileField(blank=True, upload_to='topografiya/static/files/history', verbose_name='Tarix fayli')),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
                ('object', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='historyobject', to='topografiya.object')),
            ],
            options={
                'verbose_name_plural': 'History',
            },
        ),
        migrations.CreateModel(
            name='AktPolevoyForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_polevoy_work', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
                ('object', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sktpolevoyobject', to='topografiya.object')),
            ],
            options={
                'verbose_name_plural': 'AktPolevoyForm',
            },
        ),
        migrations.CreateModel(
            name='AktKomeralForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_komeral_work', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
                ('object', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='aktkomeralobject', to='topografiya.object')),
            ],
            options={
                'verbose_name_plural': 'AktKomeralForm',
            },
        ),
    ]
