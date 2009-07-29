from django.contrib import admin
from mycitybikes.models import City, Provider, BikeStation

admin.site.register(City)
admin.site.register(Provider)
admin.site.register(BikeStation)