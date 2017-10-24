# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

def index(request):
    if 'user_id' not in request.session: #if you have a user_id in session, then you assume they are logged in and thus redirect to the show page. Else they should try logging in again
        return render(request,'loginandregistration/index.html')
    else:
        return redirect('/show')

def register(request):
    res = User.objects.valid_register(request.POST) #you want to store the response that you're geting from the register method in the manager
    if res['status']: #if your response has a status (because status was a true false if there were messages or not)
        user = User.objects.create_user(request.POST) #create the user with the data and store their shit into the user variable
        request.session['user_id'] = user.id #put their id in session and redirect show
        return redirect('/show')
    else:
        for error in res['errors']: #if errors are found, loop through them and show them all
            messages.error(request,error)
        return redirect('/')

def login(request):
    user = User.objects.login(request.POST) #go into the user model, and find the method login. Pass all your data into it (whatever the request post is)
    if user: #this is what it returns
        request.session['user_id'] = user.id #if it returns a user, store their id into the session id method and route to the show page
        return redirect('/show')
    messages.error(request,"email or password invalid") #else, tell them that they done fucked up
    return redirect('/')

def logout(request):
    request.session.clear() #just clears session
    return redirect('/')

def success(request): #do check for session, don't pass id into route parameter to render
    data = {
        "shit": User.objects.get(id=request.session['user_id']) #get all of the users data from the database and store into a dictionary
    }
    return render(request,'loginandregistration/show.html',data) #pass that dictionary so that you can render some shit
