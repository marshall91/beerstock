from django.contrib import admin
from beers.models import Brewery, Type ,Beer

admin.site.register(Beer)
admin.site.register(Brewery)
admin.site.register(Type)