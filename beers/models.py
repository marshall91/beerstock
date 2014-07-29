from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

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
    untappdAuth = models.CharField(max_length=1000, default=None, null=True, blank=True)
    mobileAppAuth = models.CharField(max_length=1000, default=None, null=True, blank=True)
    gmtOffset = models.IntegerField(default=-8)
    timezone = models.CharField(max_length=10, default='PST')


def JsonToBeer(entry):
    new_beer = BeerTable()
    new_beer.untappdId = entry['beer']['bid']
    new_beer.name = entry['beer']['beer_name']
    new_beer.style = entry['beer']['beer_style']
    new_beer.imgUrl = entry['beer']['beer_label']
    new_beer.abv = entry['beer']['beer_abv']
    new_beer.breweryName = entry['brewery']['brewery_name']
    new_beer.breweryId = entry['brewery']['brewery_id']
    try:
        db_beer = BeerTable.objects.get(untappdId=new_beer.untappdId)
    except ObjectDoesNotExist:
        new_beer.save()
    db_beer = BeerTable.objects.get(untappdId=new_beer.untappdId)
    new_beer.id = db_beer.id

    return new_beer