from django.contrib import admin

from locations.models import City, State, StateZone, Country, CityZone


class CountryAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['name']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    list_per_page = 25


class StateAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_display = ['id', 'name', 'country', 'created_at']
    list_display_links = ['name']
    list_filter = ['is_active', 'country__name']
    search_fields = ['name', 'code']
    raw_id_fields = ['country']
    list_per_page = 25


class CityAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_display = ['id', 'name', 'state', 'created_at']
    list_filter = ['is_active', 'state__name']
    search_fields = ['name']
    list_per_page = 25


class StateZoneAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_display = ['id', 'unique_id', 'state', 'created_at']
    list_display_links = ['unique_id']
    list_per_page = 25

class CityZone(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_display = ['id','city', 'state_zone']
    list_per_page = 25


admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(StateZone, StateZoneAdmin)
