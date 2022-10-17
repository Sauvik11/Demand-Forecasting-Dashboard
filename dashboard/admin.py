from django.contrib import admin

from dashboard.models import Forecast_Master, Weather,corr_dates,Weather24

admin.site.register(Forecast_Master)

admin.site.register(Weather)
admin.site.register(corr_dates)
admin.site.register(Weather24)