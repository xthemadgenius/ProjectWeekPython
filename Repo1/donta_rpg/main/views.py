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
    return render(request, "select.html")

def character_details(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "character": Character.objects.get(id=request.session['character_id']),
        "items": Item.objects.get(id=request.session['item_id']),
    }
    return render(request, 'character_detail.html', context)

def chosen(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'admin.html', context)

def chosen_create_character(request):
    user = User.objects.get(id=request.session['user_id'])
    Character.objects.create(
        name=request.POST['name'],
        ability=request.POST['ability'],
        attack=request.POST['attack'],
        health=request.POST['health'],
        user=user,
    )
    return redirect('/character')

def chosen_create_item(request):
    character = Character.objects.get(id=request.session['user_id'])
    this_item = Item.objects.create(
        item_name=request.POST['item_name'],
        item_effect=request.POST['item_effect'],
        special_ability=request.POST['special_ability'],
        character=character
    )
    request.session['item_id'] = this_item.id
    return redirect('/character')

def chosen_create_obstacle(request):
    item = Item.objects.get(id=request.session['item_id'])
    Obstacle.objects.create(
        obstacle_name=request.POST['obstacle_name'],
        health=request.POST['health'],
        item=item,
    )
    return redirect('/character')

def logout(request):
    request.session.clear()
    return redirect('/')


# test code to view Other Pages
def game(request):
    return render(request, 'game.html')

def boss(request):
    return render(request, 'boss.html')

def main_game(request):
    return render(request, 'game2.html')
    
def player(request):
    return render(request, 'character_detail.html')

def shop(request):
    return render(request, 'shop.html')
