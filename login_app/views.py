from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt
# Create your views here.

def index(request):
    return render(request, "login.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/login')
    else:
        password = request.POST['user_pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)
        request.session['user_id'] = new_user.id
        return redirect('/')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['user_pw'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/')
        else:
            messages.error(request, "Password does not match!")
            return redirect('/login')
    else:
        messages.error(request, 'There is no user with that email address!')
        return redirect('/login')

def logout(request):
    del request.session['user_id']
    return redirect('/login')