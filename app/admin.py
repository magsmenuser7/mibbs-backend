from django.contrib import admin
from .models import UserProfile

# Register your models here.


class AdminUserProfile(admin.ModelAdmin):
    list_display=['name','email','password']




admin.site.register(UserProfile,AdminUserProfile)
