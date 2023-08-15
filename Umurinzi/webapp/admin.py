""" Adding model to admin dashbord"""
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Item)
admin.site.register(Image)
admin.site.register(SpecialId)
admin.site.register(ItemCategory)
admin.site.register(SubCategory)
admin.site.register(Report)
