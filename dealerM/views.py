from django.shortcuts import render, redirect
from .models import Dealer, WholesaleDeal, RetailCarInventory
from manufacturerM.models import Manufacturer, Blueprint
from customerM.models import RetailDeal, CarsOwned
from django.db import transaction

# Create your views here.

def dealerHome(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='dealer':
        return redirect('/')
    else:
        u = Dealer.objects.get(pk=request.session['user'])
        r = RetailCarInventory.objects.filter(dealer=u)
    
        dataToFrontend = {'user': u}
        dataToFrontend['retails'] = r
        
        if ('sMessage' in request.session.keys()):
            dataToFrontend['success'] = request.session['sMessage']
            del request.session['sMessage']

        if ('eMessage' in request.session.keys()):
            dataToFrontend['error'] = request.session['eMessage']
            del request.session['eMessage']

        wholesaleNotRejections = WholesaleDeal.objects.filter(dealer=u, isRejected=False)
        wholesalesRejections = WholesaleDeal.objects.filter(dealer=u, isRejected=True)

        if len(wholesalesRejections)!=0:
            dataToFrontend['wholesalesRejections'] = wholesalesRejections
        
        if len(wholesaleNotRejections)!=0:
            dataToFrontend['wholesaleNotRejections'] = wholesaleNotRejections

        rd = RetailDeal.objects.filter(dealer=u, isRejected=False)
        if len(rd)!=0:
            dataToFrontend['retailDeals'] = rd

        return render(request, 'dealer/dealerHome.html', dataToFrontend)

def wholesaleDeal(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='dealer':
        return redirect('/')
    else:
        u = Dealer.objects.get(pk=request.session['user'])
        Ms = Manufacturer.objects.all()
        dataToFrontend = {'user': u, 'manufacturers': Ms}
        dataToFrontend['cars'] = Blueprint.objects.all()
        return render(request, 'dealer/wholesaleDeal.html', dataToFrontend)

def create_wholesale_deal(request):
    m = int(request.POST['manufacturer'])
    carNameId = request.POST['carNameId']
    count = request.POST['count']

    u = Dealer.objects.get(pk=request.session['user'])
    m = Manufacturer.objects.get(pk=m)
    car = Blueprint.objects.get(pk=carNameId)

    try:
        w = WholesaleDeal(manufacturer=m, dealer=u, carBlueprint=car, amount=count, isRejected=False)
        w.save()
    except:
        request.session['eMessage'] = 'Wholesale deal was not created successfully.'
    else:
        request.session['sMessage'] = 'Wholesale deal was created successfully.'

    return redirect('dealerHome')

def addBalance(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='dealer':
        return redirect('/')
    else:
        u = Dealer.objects.get(pk=request.session['user'])
        dataToFrontend = {'user': u}

        return render(request, 'dealer/addBalance.html', dataToFrontend)

def add_balance(request):
    u = Dealer.objects.get(pk=request.session['user'])
    deposit = float(request.POST['deposit'])

    u.balance += deposit
    u.save()
    
    request.session['sMessage'] = 'Money was deposited successfully.'
    
    return redirect('dealerHome')

def retail_deal(request, id):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='dealer':
        return redirect('/')
    else:
        u = Dealer.objects.get(pk=request.session['user'])
        r = RetailCarInventory.objects.filter(dealer=u)
        rd = RetailDeal.objects.get(pk=id)
        dataToFrontend = {'user': u, 'retail': rd}
        if len(r)>0:
            dataToFrontend["retailStock"] = r
        return render(request, 'dealer/moreOnRetailDeal.html', dataToFrontend)

@transaction.atomic
def process_retail_deal(request):
    status = request.POST['status']
    retailId = request.POST['retailId']

    dealer = Dealer.objects.get(pk=request.session['user'])
    retail = RetailDeal.objects.get(pk=retailId)
    car = retail.carBlueprint

    if status=="decline":
        try:
            retail.isRejected = True
            retail.save()
        except:
            request.session['eMessage'] = 'Something went wrong...'
        else:
            request.session['sMessage'] = 'Retail deal had been declined.'

        return redirect('dealerHome')
    
    elif status=="accept":
        inventory = RetailCarInventory.objects.filter(dealer=dealer, carBlueprint=car)
        
        if len(inventory)>0:
            inventory = inventory[0]
            # Check for money availability
            if retail.customer.balance<car.cost:
                request.session['eMessage'] = 'Customer has no enough money.'
                return redirect('dealerHome')
            
            # Proceed the logic
            if inventory.count==1:
                inventory.delete()
            else:
                inventory.count -= 1
                inventory.save()
            
            dealer.balance += car.cost
            dealer.save()

            retail.customer.balance -= car.cost
            retail.customer.save()

            i, created = CarsOwned.objects.get_or_create(customer=retail.customer, carBlueprint=car)
            if created:
                i.count = 1
            else:
                i.count += 1
            i.save()
            
            retail.delete()

            request.session['sMessage'] = 'You have accepted the retail deal.'

            return redirect('dealerHome')
        else:
            request.session['eMessage'] = 'Out of stock.'
            return redirect('dealerHome')
