import json
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import random

from beers.models import BeerTable, StockTable, HistoryTable, MemberTable
from Untappd import *

from django.views.decorators.csrf import csrf_exempt, csrf_protect
import sys


def serialize_beer(beer):
    json_beer = {}
    json_beer['untappdId'] = beer.untappedId
    json_beer['name'] = beer.name
    json_beer['style'] = beer.style
    json_beer['imgUrl'] = beer.imgUrl
    json_beer['abv'] = beer.abv
    json_beer['breweryName'] = beer.breweryName
    json_beer['breweryId'] = beer.breweryId
    return json_beer

def serialize_stock(stock):
    json_stock = {}
    json_stock['owner'] = stock.owner.id
    json_stock['untappdId'] = stock.untappdId
    json_stock['beerName'] = stock.beerName
    json_stock['amountInStock'] = stock.amountInStock
    json_stock['amountDrank'] = stock.amountDrank
    json_stock['notes'] = stock.notes
    return json_stock


@csrf_exempt
def auth(request):
    response_data = {}
    if request.method == "POST":
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            token = random.randint(0, sys.maxint)
            try:
                member = MemberTable.objects.get(user=user)
            except ObjectDoesNotExist:
                member = MemberTable(user=user)
            member.mobileAppAuth = token
            member.save()
            response_data['result'] = 'success'
            response_data['token'] = token
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['result'] = 'failed'
            response_data['message'] = 'Invalid Credentials'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['result'] = 'failed'
        response_data['message'] = 'Authentication requires post requests'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def get_stock(request):
    response_data = {}
    owner = request.GET.get('ownerId')
    token = request.GET.get('token')
    try:
        compareToken = MemberTable.objects.get(user=owner).mobileAppAuth
    except ObjectDoesNotExist:
        compareToken = None
    if token == compareToken:
        beer_list = StockTable.objects.filter(owner=owner, amountInStock__gt=0)
        count = 0
        response_data['beers'] = {}
        for beer in beer_list:
            response_data['beers'][count] = serialize_beer(beer)
            count += 1
        response_data['result'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['result'] = 'failed'
        response_data['message'] = 'Failed token authentication'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def get_beer_stock(request, bid):
    response_data = {}
    owner = request.GET.get('ownerId')
    token = request.GET.get('token')
    try:
        compareToken = MemberTable.objects.get(user=owner).mobileAppAuth
    except ObjectDoesNotExist:
        compareToken = None
    print compareToken
    print token
    if token == compareToken:
        stock = StockTable.objects.get(owner=owner, untappdId=bid)
        response_data['stock'] = serialize_stock(stock)
        response_data['result'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['result'] = 'failed'
        response_data['message'] = 'Failed token authentication'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def get_beer(request, bid):
    beer = BeerTable.objects.get(untappdId=bid)
    serialized_beer = serializers.serialize('json', [ beer, ])
    return HttpResponse(serialized_beer, content_type="application/json")