from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from . models import *

def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    validatorErrors = User.objects.basicValidator(request.POST)
    print("********", validatorErrors)
    if len(validatorErrors) > 0:
        for key, value in validatorErrors.items():
            messages.error(request, value)
        return redirect('/')

    hash1 = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()

    newuser = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = hash1)

    request.session['loggedInUserId']= newuser.id

    return redirect('/wishes')

def wishes(request):
    if 'loggedInUserId' not in request.session:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('/')
    context = {
        'loggedinUser': User.objects.get(id=request.session['loggedInUserId']),
        'allWishes': Wish.objects.all(),
        'userwishes': Wish.objects.exclude(user=request.session['loggedInUserId'])
    }
    return render(request, "wishes.html",context)

def newWish(request):
    context = {
        'loggedinUser': User.objects.get(id=request.session['loggedInUserId']),
        'allWishes': Wish.objects.all(),
    }
    return render(request, "newWish.html",context)

def wished(request, userid):
    errorsFromValidator = Wish.objects.wishValidator(request.POST)

    if len(errorsFromValidator) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    
    Wish.objects.create(wish=request.POST['wish'], desc=request.POST['desc'], user= User.objects.get(id=userid))
    return redirect('/wishes')

def delete(request, wishid):
    wish = Wish.objects.get(id=wishid)
    wish.delete()
    return redirect('/wishes')

def edit(request, wishid):
    context = {
        'someWish': Wish.objects.get(id=wishid),
        'loggedinUser': User.objects.get(id=request.session['loggedInUserId'])
    }
    return render(request,"edit.html",context)

def update(request, wishid):
    validatorErrors = User.objects.editValidator(request.POST)

    if len(validatorErrors) > 0:
        for key, value in validatorErrors.items():
            messages.error(request, value)
        return redirect(f'/edit/{wishid}')

    wish = Wish.objects.get(id=wishid)
    wish.wish = request.POST['wish']
    wish.desc = request.POST['desc']
    wish.save()
    return redirect('/wishes')

def grant(request, wishid):
    wish = Wish.objects.get(id=wishid)
    wish.granted = True
    wish.save()
    return redirect('/wishes')

def like(request, wishid):
    this_user = User.objects.get(id=request.session['loggedInUserId'])
    this_wish = Wish.objects.get(id=wishid)

    this_wish.liked.add(this_user)

    return redirect('/wishes')

def stats(request):
    context = {
        'loggedinUser': User.objects.get(id=request.session['loggedInUserId']),
        'allWishes': Wish.objects.all(),
        'truewishes': Wish.objects.filter(user=request.session['loggedInUserId'],granted=True),
        'grantedwishes': Wish.objects.filter(granted=True),
        'pendingwishes':Wish.objects.filter(user=request.session['loggedInUserId'],granted=False)
    }
    return render (request, "stats.html",context)

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    validatorErrors = User.objects.loginValidator(request.POST)

    if len(validatorErrors) > 0:
        print(request.POST)
        for key, value in validatorErrors.items():
            messages.error(request, value)
        return redirect('/')
    
    verifyEmail = User.objects.filter(email=request.POST['email'])
    request.session['loggedInUserId']= verifyEmail[0].id

    return redirect('/wishes')
# Create your views here.
