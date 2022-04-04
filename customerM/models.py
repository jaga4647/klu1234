from django.db import models
from django.contrib.auth.models import User
from dealerM.models import Dealer
from manufacturerM.models import Blueprint


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()
    country = models.TextField()
    balance = models.FloatField()
    
    def __repr__(self):
        return "Customer: " + str(self.user)
    
    def __str__(self):
        return "Customer: " + str(self.user)

class RetailDeal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    carBlueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    isRejected = models.NullBooleanField(default=False)
    
    def __repr__(self):
        return "Retail Deal: " + str(self.customer) + " | " + str(self.dealer) + " | " + str(self.carBlueprint) + " | " + str(self.isRejected)
    
    def __str__(self):
        return "Retail Deal: " + str(self.customer) + " | " + str(self.dealer) + " | " + str(self.carBlueprint) + " | " + str(self.isRejected)

class CarsOwned(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    carBlueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

    def __repr__(self):
        return "Owned car record " + str(self.customer) + " | " + str(self.carBlueprint) + " | " + str(self.count)
    
    def __str__(self):
        return "Owned car record " + str(self.customer) + " | " + str(self.carBlueprint) + " | " + str(self.count)