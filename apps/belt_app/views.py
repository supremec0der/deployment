from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
import bcrypt

def flash_errors(errors, request):

    for error in errors:
        messages.error(request, error)

def index(request):

    print('#####################login loaded')
    return render(request, 'belt_app/index.html')

def register(request):

    if request.method == "POST":

        ##### Form Validation
        errors = User.objects.validate_registration(request.POST)

        ##### Check if errors don't exist
        if not errors:
            #####Creates the user
            hashed = bcrypt.hashpw(request.POST['register_password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = request.POST['register_firstname'], last_name = request.POST['register_lastname'], email = request.POST['register_email'], password = hashed)

            print("#################i am here and this is the user", user)

            ##### Log in the user
            request.session['user_id'] = user.id


            return redirect('/dashboard')
        
        #### Flash errors
        flash_errors(errors, request)

        return redirect('/')

def login(request):
    
    if request.method == "POST":

        errors = User.objects.validate_login(request.POST)

        if not errors:

            user = User.objects.get(email=request.POST['login_email'])
            
            if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):

                request.session['first_name'] = user.first_name
                request.session['user_id'] = user.id 

                return redirect("/dashboard")
            
            else:

                errors.append("Password do not match.")
            
        flash_errors(errors, request)
    
    return redirect('index')

def dasboard(request):

    print("########################### i am here")
    if 'user_id' in request.session:

        user = User.objects.get(id = request.session['user_id'])
        quotes = Quote.objects.all()

        context ={
            'user': user,
            'quotes': quotes
        }

        return render(request, 'belt_app/dashboard.html', context)

    return redirect('/index')

def add_quote(request):

    print(request.POST)
    user = User.objects.get(id = request.session['user_id'])

    if request.method == 'POST':

        errors = Quote.objects.quote_validator(request.POST)
        print(errors)

        if len(errors):

            for key, value in errors.items():

                messages.error(request,value)

            return redirect("/dashboard")

        else:

            newQuote = Quote.objects.create( content = request.POST['content'], author = request.POST['author'], uploader = User.objects.get(id=request.session['user_id']))
            
    return redirect("/dashboard")

def user(request, id):

    user = User.objects.get(id=id)
    quotes = User.objects.get(id=id).uploaded_quotes.all()

    context = {
        'user' : user,
        'quotes' : quotes
    }

    return render(request,'belt_app/view.html', context)

def like(request):

    user = User.objects.get(id = request.session['user_id'])
    quote = Quote.objects.get(id = request.POST['quote_id'])

    if request.method == 'POST':

        errors = Like.objects.review_validator(request.POST)
        print(errors)

        if len(errors):

            for key, value in errors.items():

                messages.error(request,value)

        if User.objects.get(id = request.session['user_id']).likes.filter(quote_id = request.POST['quote_id']):

            return redirect("/dashboard")

        else:

            newLike = Like.objects.create(user = user, quote = quote)
            
    return redirect("/dashboard")

def edit(request, id):

    user = User.objects.get(id=id)
    context ={
        'user' : user
    }

    return render(request, 'belt_app/edit.html', context)

def update(request):

    if request.method == 'POST':

        id = request.POST['user_id']
        errors = User.objects.update_validator(request.POST)
        print(errors)

        if not errors:
            
            editUser = User.objects.get(id=id)
            editUser.first_name = request.POST['first_name']
            editUser.last_name = request.POST['last_name']
            editUser.email = request.POST['email']
            editUser.save()

            return redirect("/dashboard")

        flash_errors(errors, request)
    
    return redirect('/edit')

def delete(request, id):
    
    d = Quote.objects.get(id=id)
    d.delete()

    return redirect('/dashboard')

def logout(request):

    request.session.clear()

    return redirect(reverse('index'))