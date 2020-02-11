# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('drawing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aoi',
            name='geometry_final',
            field=django.contrib.gis.db.models.fields.GeometryField(srid=3857, null=True, verbose_name='Final Polygon Geometry', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aoi',
            name='geometry_orig',
            field=django.contrib.gis.db.models.fields.GeometryField(srid=3857, null=True, verbose_name='Original Polygon Geometry', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='windenergysite',
            name='geometry_final',
            field=django.contrib.gis.db.models.fields.GeometryField(srid=3857, null=True, verbose_name='Final Polygon Geometry', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='windenergysite',
            name='geometry_orig',
            field=django.contrib.gis.db.models.fields.GeometryField(srid=3857, null=True, verbose_name='Original Polygon Geometry', blank=True),
            preserve_default=True,
        ),
    ]
