from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import John, Review

@admin.register(John)
class JohnAdmin(OSMGeoAdmin):
    list_display = ('id', 'name', 'address', 'display_name', 'city', 'county', 'state', 'location')

@admin.register(Review)
class ReviewAdmin(OSMGeoAdmin):
    list_display = ('id', 'user', 'john', 'rating', 'timestamp')
