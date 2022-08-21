from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from locations.models import State,StateZone
from django.forms import ModelChoiceField
class StateForm(forms.Form):
    state=forms.ModelChoiceField(queryset=State.objects.all())

class NameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        
        return obj.get_discom()
class DiscomForm(forms.Form):
    zones=forms.ModelChoiceField(queryset=StateZone.objects.filter(state_id=3), to_field_name="discom")