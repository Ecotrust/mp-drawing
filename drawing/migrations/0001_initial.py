# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name=b'Date Modified')),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('manipulators', models.TextField(help_text=b'csv list of manipulators to be applied', null=True, verbose_name=b'Manipulator List', blank=True)),
                ('geometry_orig', django.contrib.gis.db.models.fields.PolygonField(srid=3857, null=True, verbose_name=b'Original Polygon Geometry', blank=True)),
                ('geometry_final', django.contrib.gis.db.models.fields.PolygonField(srid=3857, null=True, verbose_name=b'Final Polygon Geometry', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('content_type', models.ForeignKey(related_name='drawing_aoi_related', blank=True, to='contenttypes.ContentType', null=True)),
                ('sharing_groups', models.ManyToManyField(related_name='drawing_aoi_related', editable=False, to='auth.Group', blank=True, null=True, verbose_name=b'Share with the following groups')),
                ('user', models.ForeignKey(related_name='drawing_aoi_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AOI',
                'verbose_name_plural': 'AOIs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WindEnergySite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name=b'Date Modified')),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('manipulators', models.TextField(help_text=b'csv list of manipulators to be applied', null=True, verbose_name=b'Manipulator List', blank=True)),
                ('geometry_orig', django.contrib.gis.db.models.fields.PolygonField(srid=3857, null=True, verbose_name=b'Original Polygon Geometry', blank=True)),
                ('geometry_final', django.contrib.gis.db.models.fields.PolygonField(srid=3857, null=True, verbose_name=b'Final Polygon Geometry', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('content_type', models.ForeignKey(related_name='drawing_windenergysite_related', blank=True, to='contenttypes.ContentType', null=True)),
                ('sharing_groups', models.ManyToManyField(related_name='drawing_windenergysite_related', editable=False, to='auth.Group', blank=True, null=True, verbose_name=b'Share with the following groups')),
                ('user', models.ForeignKey(related_name='drawing_windenergysite_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
