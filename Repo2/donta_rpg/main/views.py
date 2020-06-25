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
    return redirect('/dashboard')

def login(request):
    users = User.objects.filter(email=request.POST['email'])
    if users:
        log_in_user = users[0]
        if  bcrypt.checkpw(request.POST['password'].encode(), log_in_user.password.encode()):
            request.session['user_id'] = log_in_user.id
            return redirect('/dashboard')
    messages.error(request, "Email and/or Password not found")
    return redirect('/')
    
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_characters": Character.objects.all(),
        "all_items": Item.objects.all(),
    }
    return render(request, 'dashboard.html', context)

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
        attack=request.POST['attack'],
        health=request.POST['health'],
        ability=request.POST['ability'],
        user=user,
    )
    return redirect('/dashboard')

def chosen_create_item(request):
    character = Character.objects.get(id=request.session['user_id'])
    this_item = Item.objects.create(
        item_name=request.POST['item_name'],
        attack=request.POST['attack'],
        health=request.POST['health'],
        special_ability=request.POST['special_ability'],
        character=character,
    )
    request.session['item_id'] = this_item.id
    return redirect('/dashboard')

def chosen_create_obstacle(request):
    item = Item.objects.get(id=request.session['item_id'])
    Obstacle.objects.create(
        obstacle_name=request.POST['obstacle_name'],
        health=request.POST['health'],
        item=item,
    )
    return redirect('/dashboard')

def chosen_create_enemy(request):
    Enemy.objects.create(
        enemy_name=request.POST['enemy_name'],
        name=request.POST['name'],
        attack=request.POST['attack'],
        health=request.POST['health'],
        ability=request.POST['ability'],
    )
    return redirect('/dashboard')

def select(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request, "select.html", context)

# def get_character(request, character_id):
#     character = Character.get(id=character_id)
#     return redirect('/game')
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

def logout(request):
    request.session.clear()
    return redirect('/')
