from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"
        user = User.objects.filter(email = postData['email'])
        if user:
            errors['email'] = "There is already a registered user with that email!"
        if len(postData['user_pw']) < 8 or postData['user_pw'] != postData['user_confirm_pw']:
            errors['user_pw'] = "Passwords must be at least 8 characters and match!"
        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length = 255, blank = False)
    last_name = models.CharField(max_length = 255, blank = False)
    email = models.CharField(max_length = 255, blank = False, unique = True)
    password = models.CharField(max_length = 255, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
