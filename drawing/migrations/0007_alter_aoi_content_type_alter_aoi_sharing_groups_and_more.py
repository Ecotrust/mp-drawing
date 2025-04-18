# Generated by Django 4.2 on 2024-02-28 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drawing', '0006_auto_20211216_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aoi',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='sharing_groups',
            field=models.ManyToManyField(blank=True, editable=False, related_name='%(app_label)s_%(class)s_related', to='auth.group', verbose_name='Share with the following groups'),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='windenergysite',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='windenergysite',
            name='sharing_groups',
            field=models.ManyToManyField(blank=True, editable=False, related_name='%(app_label)s_%(class)s_related', to='auth.group', verbose_name='Share with the following groups'),
        ),
        migrations.AlterField(
            model_name='windenergysite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
    ]
