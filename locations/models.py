from django.db import models
from django.utils.text import gettext_lazy as _

from dashboard.utils.models import BaseModel


class Country(BaseModel):
    name = models.CharField(_("country name"), max_length=100)
    code = models.CharField(_("country code"), max_length=10)

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return f"{self.name}"


class State(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(_("state name"), max_length=200)
    code = models.CharField(_("state code"), max_length=10)
    unique_id = models.CharField(_("state unique id"), max_length=200, null=True, blank=True)
    zone = models.CharField(_("zone name"), max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class City(BaseModel):
    name = models.CharField(_('city name'), max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    geocode= models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('cities')

    def __str__(self):
        return f"{self.name}"


class StateZone(BaseModel):
    unique_id = models.CharField(max_length=100, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    discom = models.CharField(max_length=10, default="00")
    zone = models.CharField(max_length=10, default="00")
    city_code = models.CharField(max_length=10, default="00")

    def __str__(self):
        return f"{self.unique_id}"


class CityZone(BaseModel): 
    city =models.CharField(max_length=50, default="00")
    state_zone= models.CharField(max_length=50, default="00")

    def __str__(self):
        return f"{self.city}"


    
