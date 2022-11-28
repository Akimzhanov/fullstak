from django.contrib import admin
from .models import Category, Smart, SmartImage


class TabularInlineImage(admin.TabularInline):
    model = SmartImage
    extra = 0
    fields = ['image']


class LaptopAdmin(admin.ModelAdmin):
    model = Smart
    inlines = [TabularInlineImage, ]


admin.site.register(Smart, LaptopAdmin)
admin.site.register(Category)