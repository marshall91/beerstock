from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.


class BeerTable(models.Model):
    untappdId = models.IntegerField()
    name = models.CharField(max_length=200)
    style = models.CharField(max_length=200)
    imgUrl = models.CharField(max_length=200)
    abv = models.FloatField()
    breweryName = models.CharField(max_length=200)
    breweryId = models.CharField(max_length=200)


class StockTable(models.Model):
    owner = models.ForeignKey(User)
    untappdId = models.IntegerField()
    beerName = models.CharField(max_length=200)
    amountInStock = models.IntegerField()
    amountDrank = models.IntegerField()
    notes = models.CharField(max_length=1000)


class HistoryTable(models.Model):
    owner = models.ForeignKey(User)
    untappdId = models.IntegerField()
    beerName = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=1000)


class MemberTable(models.Model):
    user = models.ForeignKey(User)
    untappdAuth = models.CharField(max_length=1000, defaul=None)
    mobileAppAuth = models.CharField(max_length=1000, default=None)
    gmtOffset = models.IntegerField(default=-8)
    timezone = models.CharField(max_length=10, default='PST')
