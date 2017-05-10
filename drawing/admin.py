from django.contrib.gis import admin
from .models import AOI, WindEnergySite

admin.site.register(AOI, admin.OSMGeoAdmin)
admin.site.register(WindEnergySite, admin.OSMGeoAdmin)
