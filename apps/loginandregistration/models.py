# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt, re
from datetime import datetime
from time import strftime,localtime
#EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
#PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
from django.db import models

#the only shit you should have in views are redirect/render and session or flash in VIEWS. All else in models

class UserManager(models.Manager): #this is the django models.manager class which we inherit from. Extending shit to this for more functionality
    def login(self,post):#this is getting all the shit from your form for checking
        email = post['login_email'].lower() #this gets the login email and stores it into a variable
        users = self.filter(email = email) #this queries the database and returns a list of emails that match the email that was passed in    
        if users: #if that list has users, take the first one (because we expect the lsit to only have one dude)
            user = users[0] #set the first dude to a user variable
            if bcrypt.checkpw(post['login_password'].encode(),user.password.encode()): #if you found an email address, then do a check using bcrypty
                return user #you want to return the user to the function so that they can parse their shit and display on the template
        return False #else, you done fucked up
        

    def valid_register(self, post): #pass in self because OOP, how can I explain it
        email = post['email'].lower()  #this is getting all the shit from your form for checking
        name = post['name']
        alias = post['alias']
        cpassword = post['cpassword']
        password = post['password']
        
        errors = [] #create empty array and append fails into this

        if len(password) < 8:
            errors.append('Password too few characters yo')
        elif cpassword != password:
            errors.append('Passwords dont match yo')

        if len(name) < 3:
            errors.append("Your name cannot be that short yo")    
        
        return {'status': len(errors) == 0, 'errors':errors} #this says return a dictionary of the "errors" array and a status. If the length of arrays is 0
    
    def create_user(self,post): #this method creates the actual user
        email = post['email'].lower()  #this is getting all the shit from your form for checking
        name = post['name']
        alias = post['alias']
        password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt()) #collect the password
        return self.create(name=name, alias=alias, password=password, email=email ) #throw that shit into the database query of "create" and it'll put it into the db

    def add_friend(self,user_id,friend_id):
        user = User.objects.get(id=user_id)
        friend = User.objects.get(id=friend_id)
        user.friended.add(friend)
        return friend
    
    def remove_friend(self,user_id,friend_id):
        user = User.objects.get(id=user_id)
        friend = User.objects.get(id=friend_id)
        user.friended.remove(friend)
        return friend
        

    def show_friends(self,user_id):
        user = User.objects.get(id = user_id)
        other_users = User.objects.all()
        data = {
            "user" : user,
            "my_friends" : other_users.filter(friended=user),
            "other_friends" : other_users.exclude(friended=user),
            "count_of_myfriends" : len(other_users.filter(friended=user))
        }
        return data

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    password = models.CharField(max_length=255)
    friended = models.ManyToManyField('self', related_name="friended_by")
    objects = UserManager() #this inherits from god manager now AND usermanager
    def __str__(self): #always add this so it looks prettier when printing
        return "{} {} {} {}".format(self.name,self.email,self.alias,self.password)
# Create your models here.
