# Generated by Django 3.2.8 on 2024-03-25 18:06

import apps.monitor.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
                ('code', models.CharField(max_length=20, null=True)),
                ('description', models.TextField(null=True)),
                ('created_at', apps.monitor.models.CustomDateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'reports',
            },
            managers=[
                ('custom_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ReportType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200, null=True)),
                ('url', models.TextField(null=True)),
                ('zoom', models.IntegerField(default=0)),
                ('target_iterations', models.IntegerField(default=0)),
                ('created_at', apps.monitor.models.CustomDateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'report_types',
            },
            managers=[
                ('custom_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='VmwareMachine',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('data_1', models.CharField(max_length=255)),
                ('data_2', models.CharField(max_length=255)),
                ('data_3', models.CharField(max_length=255)),
                ('data_4', models.CharField(max_length=255)),
                ('data_5', models.CharField(max_length=255)),
                ('annotation', models.CharField(max_length=255)),
                ('ip', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('ram', models.IntegerField()),
                ('processors', models.IntegerField()),
                ('sockets', models.IntegerField()),
                ('disk', models.IntegerField()),
                ('os', models.CharField(max_length=255)),
                ('lang', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'vmware_machines',
            },
            managers=[
                ('custom_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ReportScreenshot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('path', models.CharField(max_length=2000, null=True)),
                ('created_at', apps.monitor.models.CustomDateTimeField(auto_now_add=True)),
                ('report', models.ForeignKey(db_column='report_id', on_delete=django.db.models.deletion.CASCADE, to='monitor.report')),
                ('report_type', models.ForeignKey(db_column='report_type_id', on_delete=django.db.models.deletion.CASCADE, to='monitor.reporttype')),
            ],
            options={
                'db_table': 'report_screenshots',
            },
            managers=[
                ('custom_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
