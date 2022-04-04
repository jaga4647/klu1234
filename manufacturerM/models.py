from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Manufacturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()
    country = models.TextField()
    balance = models.FloatField()
    
    def __repr__(self):
        return "Manufacturer: " + str(self.user)
    
    def __str__(self):
        return "Manufacturer: " + str(self.user)

class Blueprint(models.Model):
    name = models.TextField(unique=True)
    cost = models.FloatField()

    def __repr__(self):
        return "Car model: " + self.name + " | " + str(self.cost)

    def __str__(self):
        return "Car model: " + self.name + " | " + str(self.cost)

class ManufactureInventory(models.Model):
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    carBlueprint = models.ForeignKey('Blueprint', on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

    def __repr__(self):
        return "Manufacturer Inventory record: " + str(self.manufacturer) + " | " + str(self.carBlueprint) + " | " + str(self.count)

    def __str__(self):
        return "Manufacturer Inventory record: " + str(self.manufacturer) + " | " + str(self.carBlueprint) + " | " + str(self.count)