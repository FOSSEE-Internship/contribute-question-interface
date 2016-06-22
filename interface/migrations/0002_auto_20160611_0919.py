# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-11 09:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.MultipleChoiceQuestion'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.CodeQuestion'),
        ),
    ]
