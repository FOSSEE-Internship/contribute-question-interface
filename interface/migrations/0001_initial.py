# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-03-09 12:58
from __future__ import unicode_literals

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
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('points', models.FloatField(default=1.0)),
                ('language', models.CharField(default='python', max_length=24)),
                ('type', models.CharField(default='code', max_length=24)),
                ('solution', models.TextField()),
                ('citation', models.TextField(blank=True, help_text='Please add appropriate citation                                if the question is adapted from elsewhere.', null=True)),
                ('originality', models.CharField(choices=[('original', 'Original Question'), ('adapted', 'Adapted Question')], default='original', max_length=24)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Verygood'), (5, 'Excellent')], default=3)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(choices=[(1, 'easy'), (2, 'medium'), (3, 'difficult')], max_length=24)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.Question')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='stdiobasedtestcase', max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='StdIOBasedTestCase',
            fields=[
                ('testcase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='interface.TestCase')),
                ('expected_input', models.TextField(blank=True, default=None, null=True)),
                ('expected_output', models.TextField(default=None)),
            ],
            bases=('interface.testcase',),
        ),
        migrations.AddField(
            model_name='testcase',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interface.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('user', 'question')]),
        ),
    ]
