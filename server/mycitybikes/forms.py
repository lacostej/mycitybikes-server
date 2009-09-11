from django import forms
from google.appengine.ext import db
from django.utils.translation import ugettext_lazy as _, ugettext as __
from mycitybikes.models import City, Provider, BikeStation, BikeStationStatus
from ragendja.forms import FormWithSets, FormSetField

class BikeStationForm(forms.Form):
  providerId = forms.IntegerField(min_value=0, required=False)
  name = forms.CharField(required=False, )
  description = forms.CharField(required=False)
  latitude = forms.FloatField(min_value=-90, max_value=90)
  longitude = forms.FloatField(min_value=-90, max_value=90)
  #updateDateTime = forms.RegexField() # TODO write the regex to match time isoformat
  def __init__(self, data, provider):
    super(BikeStationForm, self).__init__(data)
    self.provider = provider
  
  
  def get_geoloc(self):
    data = self.cleaned_data
    return db.GeoPt(data['latitude'], data['longitude'])
  """
  def clean_providerId(self):
    providerId = self.cleaned_data['providerId']
    provider = Provider.get_by_id(providerId)
    if not provider:
      raise  forms.ValidationError("Provider ID doesn't exists")
    self.cleaned_data['provider'] = provider"""
  
  def get_model(self):
    data = self.cleaned_data
    return BikeStation(providerRef=self.provider,
                       name= data['name'] or data['description'],
                       description=data['description'],
                       geoloc=self.get_geoloc(),
                       externalId="0")

class StatusForm(forms.Form):
  #online = forms.IntegerField(required=True, min_value=0)
  availableBikes = forms.IntegerField(required=False, min_value=0)
  freeSlots = forms.IntegerField(required=False, min_value=0)
  totalSlots = forms.IntegerField(required=False, min_value=0)
  
  def get_model(self, station):
    data = self.cleaned_data
    return BikeStationStatus(stationRef=station,
                             availableBikes=data['availableBikes'],
                             freeSlots=data['freeSlots'], totalSlots=data['totalSlots'])