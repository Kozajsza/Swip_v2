# Generated by Django 4.0.4 on 2022-06-13 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SWIPapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Asset_QR', models.CharField(default='', max_length=100)),
                ('Asset_QR_Img', models.ImageField(blank=True, null=True, upload_to='main\\static\\lessapp\\images\\qr_codes')),
                ('Type', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Make', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Model', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Serial_Number', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('CPU', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('RAM', models.FloatField(blank=True, null=True)),
                ('Storage', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Storage_Serial_Number', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Storage_Capacity', models.FloatField(blank=True, null=True)),
                ('GPU', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Motherboard_Test', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('CPU_Test', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('RAM_Test', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Wipe_Method', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Wipe_Start_Time', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Wipe_End_Time', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Wipe_Result', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Weight', models.FloatField(blank=True, null=True)),
                ('Created', models.DateTimeField(auto_now_add=True, null=True)),
                ('Updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('Ecommerce_Title', models.CharField(blank=True, default='', max_length=80, null=True)),
                ('Ecommerce_Category', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('Ecommerce_Condition', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('Ecommerce_Condition_Description', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('Ecommerce_Item_Description', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('Ecommerce_Price', models.FloatField(blank=True, null=True)),
                ('Order_Number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SWIPapp.order')),
            ],
        ),
    ]
