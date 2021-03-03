from django.db import models
from login_app.models import User

# Create your models here.

class Lead(models.Model):
    property_id = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 2)
    postal_code = models.IntegerField()
    price = models.CharField(max_length = 255)
    beds = models.IntegerField()
    baths = models.IntegerField()
    prop_type = models.CharField(max_length = 255)
    listing = models.TextField(null = True)
    investors = models.ManyToManyField(User, related_name = "leads")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    