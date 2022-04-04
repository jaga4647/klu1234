from django.contrib import admin
from .models import Dealer, WholesaleDeal, RetailCarInventory

# Register your models here.

admin.site.register(Dealer)
admin.site.register(WholesaleDeal)
admin.site.register(RetailCarInventory)