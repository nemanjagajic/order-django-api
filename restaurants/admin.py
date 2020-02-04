from django.contrib import admin
from restaurants.models import Restaurant, Food


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location',)


@admin.register(Food)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'restaurant_id',)
