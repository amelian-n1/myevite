from __future__ import unicode_literals
from django.db import models
from datetime import date
import re

class GuestManager(models.Manager):
    def guest_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = "Please enter a valid first name."
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Please enter a valid last name."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = ("Please enter a valid email address.")
        return errors

class Guest(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GuestManager()
    class Meta:
        app_label = 'first_app'
    
    @property
    def sorted_rsvps(self):
        return self.rsvps.order_by('response')

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = "Please enter a valid first name."
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Please enter a valid last name."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = ("Please enter a valid email address.")
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    class Meta:
        app_label = 'first_app'

class EventManager(models.Manager):
    def eventValidate(self, postData):
        errors={}
        if len(postData['title'])<1:
            errors['title']="Please enter a title"
        if len(postData['details'])<1:
            errors['details']="Please enter a description"
        if len(postData['date'])==False:
            errors['date']="Please enter a date"
        if len(postData['start_time'])==False:
            errors['start_time']="Please enter time"        
        if len(postData['line1'])<1:
            errors['line1']="Please enter your street address"
        if len(postData['zip'])<1:
            errors['zip']="Please enter your ZIP Code"
        if len(postData['city'])<1:
            errors['city']="Please enter your city"
        if len(postData['state'])<1:
            errors['state']="Please enter your state"
        return errors
    
class Event(models.Model):
    title = models.CharField("Title",max_length=1024)
    details = models.CharField("Details",max_length=1024)
    date = models.DateField("Date",auto_now=False,auto_now_add=False)
    start_time = models.TimeField("startTime",auto_now=False,auto_now_add=False)
    end_time = models.TimeField("endTime",auto_now=False,auto_now_add=False)
    line1 = models.CharField("Line 1",max_length=1024)
    line2 = models.CharField("Line 2",max_length=1024)
    zip = models.CharField("Zip Code",max_length=12)
    city = models.CharField("City",max_length=1024)
    state = models.CharField("State",max_length=1024)
    host = models.ForeignKey(User, related_name="events",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)    
    objects = EventManager()
    class Meta:
        app_label = 'first_app'
    
    def rsvpYesNum(self):
        return self.rsvps.filter(response="yes").count()

    def rsvpNoNum(self):
        return self.rsvps.filter(response="no").count()
    
    def rsvpMaybeNum(self):
        return self.rsvps.filter(response="maybe").count()
    
    @property
    def sorted_guest_rsvps(self):
        return self.guest.rsvps.order_by('response')


class RSVP(models.Model):
    guest = models.ForeignKey(Guest, related_name="rsvps",on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="rsvps",on_delete=models.CASCADE)
    response = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'first_app'