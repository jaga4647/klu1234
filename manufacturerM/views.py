from django.shortcuts import render, redirect
from .models import Manufacturer, Blueprint, ManufactureInventory
from dealerM.models import WholesaleDeal, RetailCarInventory
from django.db import transaction

# Create your views here.

def manufacturerHome(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='manufacturer':
        return redirect('/')
    else:
        u = Manufacturer.objects.get(pk=request.session['user'])
    
        dataToFrontend = {'user': u}
        
        if ('sMessage' in request.session.keys()):
            dataToFrontend['success'] = request.session['sMessage']
            del request.session['sMessage']

        if ('eMessage' in request.session.keys()):
            dataToFrontend['error'] = request.session['eMessage']
            del request.session['eMessage']
        
        blueprints = Blueprint.objects.all()
        if len(blueprints)!=0:
            dataToFrontend['blueprints'] = blueprints
        
        stock = ManufactureInventory.objects.filter(manufacturer=u)
        if len(stock)!=0:
            dataToFrontend['stock'] = stock

        wholesales = WholesaleDeal.objects.filter(manufacturer=u, isRejected=False)
        if len(wholesales)!=0:
            dataToFrontend['wholesaleRequests'] = wholesales

        return render(request, 'manufacturer/manufacturerHome.html', dataToFrontend)

def createBlueprint(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='manufacturer':
        return redirect('/')
    else:
        u = Manufacturer.objects.get(pk=request.session['user'])
        return render(request, 'manufacturer/createBlueprint.html', {'user': u})

def blueprint_operation(request):
    method = request.POST["method"]
    if method=="POST":
        cost = carName = request.POST['cost']
        carName = request.POST['name']
        u = Manufacturer.objects.get(pk=request.session['user'])

        try:
            b = Blueprint(name=carName, cost=cost)
            b.save()
        except:
            request.session['eMessage'] = 'Blueprint was not created successfully. Blueprint already exists.'
        else:
            request.session['sMessage'] = 'Blueprint was created successfully.'
        
        return redirect('manufacturerHome')

    elif method=="PUT":
        id = request.POST['id']
        cost = request.POST['cost']
        try:
            b = Blueprint.objects.get(pk=id)
            b.cost = float(cost)
            b.save()
        except:
            request.session['eMessage'] = 'Something went wrong...'
        else:
            request.session['sMessage'] = 'Blueprint was updated successfully.'

        return redirect('manufacturerHome')

    elif method=="DELETE":
        id = request.POST['id']
        try:
            Blueprint.objects.get(pk=id).delete()
        except:
            request.session['eMessage'] = 'Something went wrong...'
        else:
            request.session['sMessage'] = 'Blueprint was deleted successfully.'

        return redirect('manufacturerHome')

def editBlueprint(request, id):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='manufacturer':
        return redirect('/')
    else:
        u = Manufacturer.objects.get(pk=request.session['user'])
        b = Blueprint.objects.get(pk=id)
        return render(request, 'manufacturer/editBlueprint.html', {'user': u, 'blueprint': b})

def initiateOrder(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='manufacturer':
        return redirect('/')
    else:
        u = Manufacturer.objects.get(pk=request.session['user'])
        dataToFrontend = {'user': u}

        blueprints = Blueprint.objects.all()
        if len(blueprints)!=0:
            dataToFrontend['blueprints'] = blueprints

        return render(request, 'manufacturer/initiateOrder.html', dataToFrontend)

def order_created(request):
    name = request.POST['blueprint']
    count = int(request.POST['count'])
    u = Manufacturer.objects.get(pk=request.session['user'])

    blueprint = Blueprint.objects.get(name=name)

    # Check whether the manufacturer has enough money to proceed
    if u.balance<(count*blueprint.cost):
        request.session['eMessage'] = 'Not enough money to proceed the order.'
    else:
        # Proceed the transaction

        u.balance -= count*blueprint.cost
        u.save()

        i, created = ManufactureInventory.objects.get_or_create(manufacturer=u, carBlueprint=blueprint)
        if created:
            i.count = count
        else:
            i.count += count
        i.save()

        request.session['sMessage'] = 'Manufacturing order is completed. '
    
    return redirect('manufacturerHome')

def addBalance(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='manufacturer':
        return redirect('/')
    else:
        u = Manufacturer.objects.get(pk=request.session['user'])
        dataToFrontend = {'user': u}

        return render(request, 'manufacturer/addBalance.html', dataToFrontend)

def add_balance(request):
    u = Manufacturer.objects.get(pk=request.session['user'])
    deposit = float(request.POST['deposit'])

    u.balance += deposit
    u.save()
    
    request.session['sMessage'] = 'Money was deposited successfully.'
    
    return redirect('manufacturerHome')

def deal(request, id):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='manufacturer':
        return redirect('/')
    else:
        u = Manufacturer.objects.get(pk=request.session['user'])
        i = ManufactureInventory.objects.filter(manufacturer=u)
        w = WholesaleDeal.objects.get(pk=id)

        return render(request, 'manufacturer/moreOnWholesaleRequest.html', {'user': u, 'wholesale': w, 'inventory': i})

@transaction.atomic
def process_deal(request):
    status = request.POST['status']
    wholesaleId = request.POST['wholesaleId']

    manufacturer = Manufacturer.objects.get(pk=request.session['user'])
    wholesale = WholesaleDeal.objects.get(pk=wholesaleId)

    if status=="decline":
        try:
            wholesale.isRejected = True
            wholesale.save()
        except:
            request.session['eMessage'] = 'Something went wrong...'
        else:
            request.session['sMessage'] = 'Wholesale request had been declined.'

        return redirect('manufacturerHome')
    
    elif status=="accept":
        inventory = ManufactureInventory.objects.filter(manufacturer=manufacturer, carBlueprint=wholesale.carBlueprint)
        
        if len(inventory)>0:
            inventoryRecord = inventory[0]
            inventoryCount = inventory[0].count
            totalAmount = wholesale.carBlueprint.cost*wholesale.amount
            dealersBalance = wholesale.dealer.balance

            # Check availability of wholesale inventory
            if wholesale.amount>inventoryCount:
                request.session['eMessage'] = 'Not enough stock to proceed. Add stock before proceeding.'
                return redirect('manufacturerHome')

            # Check the money availability of dealers account
            if totalAmount>dealersBalance:
                request.session['eMessage'] = 'Dealer does not have enough money to proceed.'
                return redirect('manufacturerHome')
            
            # Proceed the logic
            if inventoryCount==wholesale.amount:
                inventoryRecord.delete()
            else:
                inventoryRecord.count -= wholesale.amount
                inventoryRecord.save()
            
            wholesale.dealer.balance -= totalAmount
            wholesale.dealer.save()

            manufacturer.balance += totalAmount
            manufacturer.save()

            i, created = RetailCarInventory.objects.get_or_create(dealer=wholesale.dealer, carBlueprint=wholesale.carBlueprint)
            if created:
                i.count = wholesale.amount
            else:
                i.count += wholesale.amount
            i.save()
            
            wholesale.delete()

            request.session['sMessage'] = 'You have accepted the wholesale deal.'

            return redirect('manufacturerHome')
        else:
            request.session['eMessage'] = 'Out of stock.'
            return redirect('manufacturerHome')
