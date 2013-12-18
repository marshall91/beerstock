from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
	
class Brewery(models.Model):
	name = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	uniqueBeers = models.IntegerField()
	def __unicode__(self):
		return self.name
	
class Type(models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name
	
class Beer(models.Model):
	name = models.CharField(max_length=200)
	brewery = models.ForeignKey(Brewery)
	beerType = models.ForeignKey(Type)
	amountConsumed = models.IntegerField()
	amountInFridge = models.IntegerField()
	owner = models.ForeignKey(User)
	def __unicode__(self):
		return self.name
	
class BeerForm(forms.ModelForm):
	class Meta:
		model = Beer
		exclude =('owner',)
	name = forms.CharField(label="Beer Name")
	beerType = forms.ModelChoiceField(queryset=Type.objects.all(), label="Beer Type")
	amountConsumed = forms.IntegerField(label="Amount Consumed")
	amountInFridge = forms.IntegerField(label="Amount in Fridge")
	
class BreweryForm(forms.ModelForm):
	class Meta:
		model = Brewery
		exclude =('uniqueBeers',)
	name = forms.CharField(label="Brewery Name")
	
class TypeForm(forms.ModelForm):
	class Meta:
		model = Type
	name = forms.CharField(label="Beer Type")