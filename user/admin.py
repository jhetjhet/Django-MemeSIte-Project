from django.contrib import admin

from .models import Profile, Memer
# Register your models here.

admin.site.register(Memer)
admin.site.register(Profile)