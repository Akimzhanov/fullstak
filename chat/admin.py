

from django.contrib import admin
from .models import Room, Message


admin.site.register(Room)

@admin.register(Message)
class Mess(admin.ModelAdmin):
    list_display = ('user', 'value')
