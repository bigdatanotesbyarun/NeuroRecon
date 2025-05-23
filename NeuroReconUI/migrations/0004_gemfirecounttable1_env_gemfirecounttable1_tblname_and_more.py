# Generated by Django 5.2 on 2025-04-06 21:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NeuroReconUI', '0003_alter_reconresult_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='gemfirecounttable1',
            name='env',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='gemfirecounttable1',
            name='tblname',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gztable',
            name='eapps',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='gztable',
            name='env',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='gztable',
            name='pltps',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='gztable',
            name='ps',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='jobs',
            name='env',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='jobs',
            name='executionTime',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='jobs',
            name='lastts',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='reconresult',
            name='env',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='skrecontable',
            name='env',
            field=models.CharField(default='Test', max_length=1000),
        ),
        migrations.AddField(
            model_name='skrecontable',
            name='tblname',
            field=models.CharField(default='Test', max_length=1000),
        ),
    ]
