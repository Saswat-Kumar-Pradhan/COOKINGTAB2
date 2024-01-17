from django.contrib import admin
from .models import Profile, Event, Purchase, Contribution

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile_pic')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'subject')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('event', 'profile', 'products', 'price')

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('event', 'profile', 'amount')
