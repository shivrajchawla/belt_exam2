# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt, re
from datetime import datetime
from time import strftime,localtime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
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
        cpassword = post['cpassword']
        password = post['password']
        first_name = post['first_name']
        last_name = post['last_name']

        errors = [] #create empty array and append fails into this

        if len(email) < 6 or len(email) > 30: #each validation should add to your errors array
            errors.append('Email must be 6-30char long yo')
        elif not EMAIL_REGEX.match(email):
            errors.append('Your email is invalid yo')

        if len(password) < 8:
            errors.append('Password too few characters yo')
        elif cpassword != password:
            errors.append('Passwords dont match yo')

        if len(first_name) < 2:
            errors.append("Your first name cannot be that short yo")
        elif not first_name.isalpha():
            errors.append('Your first name must be letters yo')

        if len(last_name) < 2:
            errors.append('Your last name cannot be that short yo')
        elif not last_name.isalpha():
            errors.append('Your last name must be letters yo') 
        
        
        if not errors:
            users = self.filter(email=email) # so this is querying the user table to find an email. filter returns a list of emails
            if users: #if any email exists (coming back into the variable), then that means they're already a user
                errors.append('email already taken')
        
        return {'status': len(errors) == 0, 'errors':errors} #this says return a dictionary of the "errors" array and a status. If the length of arrays is 0
    
    def create_user(self,post): #this method creates the actual user
        first_name = post['first_name'] #get shit from the form
        last_name = post['last_name']
        email = post['email'].lower() #always set the email to lower
        password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt()) #collect the password
        return self.create(first_name = first_name, email = email, last_name = last_name, password = password) #throw that shit into the database query of "create" and it'll put it into the db

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    password = models.CharField(max_length=255)
    objects = UserManager() #this inherits from god manager now AND usermanager
    def __str__(self): #always add this so it looks prettier when printing
        return "{} {} {} {}".format(self.first_name,self.last_name,self.email,self.password)
# Create your models here.
