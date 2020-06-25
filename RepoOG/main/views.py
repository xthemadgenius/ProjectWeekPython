from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Character, Item, Obstacle
from datetime import datetime
import bcrypt

def index(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    if len(errors) > 0:
        for error in errors.values():
            messages.error(request, error)
        return redirect('/')
    this_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed,
        confirm_password=hashed
    )
    request.session['user_id'] = this_user.id
    return redirect('/character')

def login(request):
    users = User.objects.filter(email=request.POST['email'])
    if users:
        log_in_user = users[0]
        if  bcrypt.checkpw(request.POST['password'].encode(), log_in_user.password.encode()):
            request.session['user_id'] = log_in_user.id
            return redirect('/character')
    messages.error(request, "Email and/or Password not found")
    return redirect('/')
    
def character(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, "character.html")

def create_character(request):
    user = User.objects.get(id=request.session['user_id'])
    this_character = Character.objects.create(
        name=request.POST['name'],
        ability=request.POST['ability'],
        bio=request.POST['bio'],
        user=user
    )
    request.session['character_id'] = this_character.id
    return redirect('/dashboard')

# def shop_manager():
#     items = {}
    

def logout(request):
    request.session.clear()
    return redirect('/')

def game(request):
    return render(request, 'game.html')

def main_game(request):
    return render(request, 'game2.html')
    
def player(request):
    return render(request, 'stats.html')

def shop(request):
    return render(request, 'shop.html')
