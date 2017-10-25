# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from ..loginandregistration.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

def index(request):
    user_id = request.session['user_id']
    friends_list = User.objects.show_friends(user_id)
    return render(request,'friends/index.html', friends_list)

def user(request,friend_id):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    friend = User.objects.get(id=friend_id)
    data = {
        "user" : user,
        "friend" : friend
    }
    return render(request,'friends/friend.html',data)

def add_friend(request,friend_id):
    user_id = request.session['user_id']
    added_friend = User.objects.add_friend(user_id,friend_id)
    data = {
        "added_friend": added_friend
    }
    #change to redirect after getting exclusion shit to work
    return redirect('/friends/')

def remove_friend(request,friend_id):
    user_id = request.session['user_id']
    removed_friend = User.objects.remove_friend(user_id,friend_id)
    data = {
        "removed_friend": removed_friend
    }
    return redirect('/friends/')

