from django.shortcuts import render, redirect
from .models import Customer, RetailDeal, CarsOwned
from manufacturerM.models import Blueprint
from dealerM.models import RetailCarInventory, Dealer
import simplejson
from django.http import HttpResponse

# Create your views here.
def customerHome(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='customer':
        return redirect('/')
    else:
        user = Customer.objects.get(pk=request.session['user'])
    
        dataToFrontend = {'user': user}

        rdpending = RetailDeal.objects.filter(customer=user, isRejected=False)
        rddeclined = RetailDeal.objects.filter(customer=user, isRejected=True)
        if len(rdpending)>0:
            dataToFrontend["retailDealsPending"] = rdpending
        if len(rddeclined)>0:
            dataToFrontend["retailDealsDeclined"] = rddeclined

        carsowned = CarsOwned.objects.filter(customer=user)
        if len(carsowned)>0:
            dataToFrontend["carsowned"] = carsowned

        
        if ('sMessage' in request.session.keys()):
            dataToFrontend['success'] = request.session['sMessage']
            del request.session['sMessage']

        if ('eMessage' in request.session.keys()):
            dataToFrontend['error'] = request.session['eMessage']
            del request.session['eMessage']

        return render(request, 'customer/customerHome.html', dataToFrontend)

def retailDeal(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='customer':
        return redirect('/')
    else:
        user = Customer.objects.get(pk=request.session['user'])
        cars = Blueprint.objects.all()
        dataToFrontend = {'user': user, 'cars': cars}
        return render(request, 'customer/retailDeal.html', dataToFrontend)

def retailDeal_process(request):
    dealerId = int(request.POST['dealer'])
    carNameId = int(request.POST['carNameId'])

    customer = Customer.objects.get(pk=request.session['user'])
    car = Blueprint.objects.get(pk=carNameId)
    dealer = Dealer.objects.get(pk=dealerId)

    try:
        RD = RetailDeal(customer=customer, dealer=dealer, carBlueprint=car, isRejected=False)
        RD.save()
    except:
        request.session['eMessage'] = 'Retail deal was not created successfully.'
    else:
        request.session['sMessage'] = 'Retail deal was created successfully.'

    return redirect('customerHome')


def addBalance(request):
    if not('role' in request.session.keys()):
        return redirect('/')

    if request.session['role']!='customer':
        return redirect('/')
    else:
        user = Customer.objects.get(pk=request.session['user'])
        dataToFrontend = {'user': user}

        return render(request, 'customer/addBalance.html', dataToFrontend)

def add_balance(request):
    user = Customer.objects.get(pk=request.session['user'])
    deposit = float(request.POST['deposit'])

    user.balance += deposit
    user.save()
    
    request.session['sMessage'] = 'Money was deposited successfully.'
    
    return redirect('customerHome')

def getDealers(request):
    blueprintId = int(request.GET["carId"])
    blueprint = Blueprint.objects.get(pk=blueprintId)
    ris = RetailCarInventory.objects.filter(carBlueprint=blueprint)

    dealers = [None]

    for ri in ris:
        dealers.append((ri.dealer.pk, ri.dealer.name))

    return HttpResponse(simplejson.dumps(dealers))
    

