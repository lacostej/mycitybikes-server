from django.contrib import admin
from mycitybikes.models import City, Provider, BikeStation, BikeStationStatus

admin.site.register(City)
admin.site.register(BikeStation)
admin.site.register(Provider)
admin.site.register(BikeStationStatus)