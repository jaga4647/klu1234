from django.db import models
from django.contrib.auth.models import User
from manufacturerM.models import Manufacturer, Blueprint

# Create your models here.

class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()
    country = models.TextField()
    balance = models.FloatField()
    
    def __repr__(self):
        return "Dealer: " + str(self.user)
    
    def __str__(self):
        return "Dealer: " + str(self.user)

class WholesaleDeal(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    carBlueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    amount = models.IntegerField()
    isRejected = models.NullBooleanField(default=False)
    
    def __repr__(self):
        return "Wholesale Deal: " + str(self.dealer) + " | " + str(self.carBlueprint) + " | " + str(self.amount) + " | " + str(self.isRejected) 
    
    def __str__(self):
        return "Wholesale Deal: " + str(self.dealer) + " | " + str(self.carBlueprint) + " | " + str(self.amount) + " | " + str(self.isRejected) 

class RetailCarInventory(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    carBlueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

    def __repr__(self):
        return "Retail Inventory Record: " + str(self.dealer) + " | " + str(self.carBlueprint) + " | " + str(self.count)
    
    def __str__(self):
        return "Retail Inventory Record: " + str(self.dealer) + " | " + str(self.carBlueprint) + " | " + str(self.count)
