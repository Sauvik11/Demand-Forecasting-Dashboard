from django.contrib import admin

from dashboard.models import Forecast_Master, Weather

admin.site.register(Forecast_Master)

admin.site.register(Weather)