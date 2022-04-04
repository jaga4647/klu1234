from django.contrib import admin

from .models import Manufacturer
from .models import Blueprint
from .models import ManufactureInventory
# Register your models here.

admin.site.register(Manufacturer)
admin.site.register(Blueprint)
admin.site.register(ManufactureInventory)