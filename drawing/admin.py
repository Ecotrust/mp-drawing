from django.contrib.gis import admin
from .models import AOI, WindEnergySite

admin.site.register(AOI, admin.GISModelAdmin)
admin.site.register(WindEnergySite, admin.GISModelAdmin)
