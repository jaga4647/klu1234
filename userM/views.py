from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from manufacturerM.models import Manufacturer
from dealerM.models import Dealer
from customerM.models import Customer

# Create your views here.

def userRegistration(request):
    if 'eMessage' in request.session.keys():
        page = render(request, 'home/userRegistration.html', {"error":request.session['eMessage']})
        del request.session['eMessage']
        return page

    elif 'sMessage' in request.session.keys():
        page = render(request, 'home/userRegistration.html', {"success":request.session['sMessage']})
        del request.session['sMessage']
        return page

    else:
        return render(request, 'home/userRegistration.html')

def signin(request):
    username = request.POST['username']
    password = request.POST['password']

    try:
        u = User.objects.get(username=username)
    except:
        request.session['eMessage'] = "User does not exist."
        return redirect('regHome')
    else:
        if not(u.check_password(password)):
            request.session['eMessage'] = "Wrong password."
            return redirect('regHome')
        else:
            # login(request, u)

            # Identify user's role
            Ms = Manufacturer.objects.filter(user=u)
            Cs = Customer.objects.filter(user=u)
            Ds = Dealer.objects.filter(user=u)

            if len(Ms)!=0:
                request.session['role'] = 'manufacturer'
                request.session['user'] = Ms[0].pk
                return redirect('/manufacturer/')

            elif len(Ds)!=0:
                request.session['role'] = 'dealer'
                request.session['user'] = Ds[0].pk
                return redirect('/dealer/')

            elif len(Cs)!=0:
                request.session['role'] = 'customer'
                request.session['user'] = Cs[0].pk
                return redirect('/customer/')



            # redirect to the associated page. TODO

def signup(request):
    role = request.POST['role']
    username = request.POST['username']
    password = request.POST['password']
    rePassword = request.POST['re-password']

    if password!=rePassword:
        request.session['eMessage'] = "Passwords are not matching."
        return redirect('regHome')

    if role=='manufacturer':
        u, created = User.objects.get_or_create(username=username)
        
        if created:
            u.set_password(password)
            u.save()

            m = Manufacturer(user=u, name=request.POST['name'], country=request.POST['country'], balance=request.POST['balance'])
            m.save()

            request.session['sMessage'] = "Manufacturer user was successfully registered"
            return redirect('regHome')
        else:
            request.session['eMessage'] = "Username already exists."
            return redirect('regHome')
    
    elif role=='dealer':
        u, created = User.objects.get_or_create(username=username)
        
        if created:
            u.set_password(password)
            u.save()

            m = Dealer(user=u, name=request.POST['name'], country=request.POST['country'], balance=request.POST['balance'])
            m.save()

            request.session['sMessage'] = "Dealer user was successfully registered"
            return redirect('regHome')
        else:
            request.session['eMessage'] = "Username already exists."
            return redirect('regHome')
    
    elif role=='customer':
        u, created = User.objects.get_or_create(username=username)
        
        if created:
            u.set_password(password)
            u.save()

            m = Customer(user=u, name=request.POST['name'], country=request.POST['country'], balance=request.POST['balance'])
            m.save()

            request.session['sMessage'] = "Customer was successfully registered"
            return redirect('regHome')
        else:
            request.session['eMessage'] = "Username already exists."
            return redirect('regHome')

def signout(request):
    del request.session['role']
    del request.session['user']
    logout(request)
    return redirect('regHome')

            
