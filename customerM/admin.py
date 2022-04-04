from django.contrib import admin
from .models import Customer, RetailDeal, CarsOwned

# Register your models here.

admin.site.register(Customer)
admin.site.register(RetailDeal)
admin.site.register(CarsOwned)