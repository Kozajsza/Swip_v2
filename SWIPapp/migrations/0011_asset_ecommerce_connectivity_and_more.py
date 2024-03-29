# Generated by Django 4.0.5 on 2022-10-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SWIPapp', '0010_hdd'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='Ecommerce_Connectivity',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='Ecommerce_Features',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='Ecommerce_FormFactor',
            field=models.CharField(blank=True, default='', max_length=35, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='Ecommerce_SuitableFor',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='Operating_System',
            field=models.CharField(blank=True, default='Not Installed', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='Screen_Size',
            field=models.CharField(blank=True, default='Not Installed', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='Storage_Type',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='Ecommerce_Category',
            field=models.CharField(blank=True, default='', max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='Ecommerce_Condition',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='Weight',
            field=models.FloatField(blank=True, default='0', null=True),
        ),
    ]
