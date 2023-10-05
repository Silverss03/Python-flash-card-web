from django.contrib import admin
from django.contrib.auth.models import User
from .models import Card

# Register your models here.
admin.site.register(Card)

# Create user and save to the database