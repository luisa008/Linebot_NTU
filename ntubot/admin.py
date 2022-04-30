from django.contrib import admin

# Register your models here.
from ntubot.models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('uid','name','section', 'part', 'hint', 'total_hint')
admin.site.register(User_Info,User_Info_Admin)
