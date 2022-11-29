from django.contrib import admin
from .models import Category, Smart, SmartImage


class TabularInlineImage(admin.TabularInline):
    model = SmartImage
    extra = 1
    fields = ['image']


class SmartAdmin(admin.ModelAdmin):
    model = Smart
    inlines = [TabularInlineImage]


admin.site.register(Smart, SmartAdmin)
admin.site.register(Category)
