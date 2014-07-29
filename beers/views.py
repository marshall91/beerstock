# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.conf import settings

from beers.models import BeerTable, StockTable, HistoryTable, MemberTable, JsonToBeer

import json
import pythonUntappd


@login_required
def search_beer(request):
    if request.method == "POST":
        beer = request.POST.get("beername", "")

        api = pythonUntappd.api(settings.UNTAPPD_CLIENT_ID, settings.UNTAPPD_CLIENT_SECRET)
        untappd_response = api.beer_search(beer)

        if untappd_response['meta']['code'] == 200:
            beer_list = []
            for entry in untappd_response['response']['beers']['items']:
                new_beer = JsonToBeer(entry)
                beer_list.append(new_beer)

            for entry in untappd_response['response']['homebrew']['items']:
                new_beer = JsonToBeer(entry)
                beer_list.append(new_beer)

            context = Context({
                'beer_list': beer_list,
                'user': request.user,
            })
            return render(request, 'beers/beer_list.html', context)
    else:
        return render(request, 'beers/stock_index.html')


@login_required
def update_beer(request, bid):
    if request.method == "POST":
        user = request.user
        beer = BeerTable.objects.get(untappdId=bid)
        new_history = request.POST.get("history", "")
        new_stock = request.POST.get("stock", "")
        try:
            stock = StockTable.objects.get(untappdId=beer.untappdId, owner=user)
        except ObjectDoesNotExist:
            stock = StockTable(amountDrank=0,amountInStock=0, owner=user, untappdId=beer.untappdId)
        stock.beerName = beer.name
        stock.amountDrank = new_history
        stock.amountInStock = new_stock
        stock.save()
        return render(request, 'beers/stock_index.html')
    else:
        beer = BeerTable.objects.get(untappdId=bid)
        try:
            stock = StockTable.objects.get(untappdId=beer.untappdId, owner=request.user)
        except ObjectDoesNotExist:
            stock = StockTable(amountDrank=0,amountInStock=0)
        context = Context({
            'beer': beer,
            'stock': stock,
            'user': request.user,
        })
        return render(request, 'beers/untappd_beer_update.html', context)


@login_required
def stock_index(request):
    user_stock_list = StockTable.objects.filter(owner=request.user, amountInStock__gt=0)
    all_beer_list = {}
    for stock in user_stock_list:
        beer = BeerTable.objects.get(untappdId=stock.untappdId)
        all_beer_list[stock.untappdId] = {'stock': stock, 'beer': beer}

    context = Context({
        'all_beer_list': all_beer_list,
        'user': request.user,
    })
    return render(request, 'beers/stock_index.html', context)


@login_required
def history_index(request):
    user_history = HistoryTable.objects.filter(owner=request.user).order_by('-timestamp')
    all_data_list = {}
    count = 0
    for history in user_history:
        beer = BeerTable.objects.get(untappdId=history.untappdId)
        all_data_list[count] = {'history': history, 'beer': beer}
        count += 1

    context = Context({
        'all_data_list': all_data_list,
        'user': request.user,
    })
    return render(request, 'beers/history_index.html', context)


@login_required
def checkout_beer(request, bid):
    beer = BeerTable.objects.get(untappdId=bid)
    stock = StockTable.objects.get(untappdId=beer.untappdId, owner=request.user)
    if request.method == "POST":
        stock.amountDrank += 1
        stock.amountInStock -= 1
        stock.save()
        history = HistoryTable(owner=request.user, untappdId=beer.untappdId, beerName=beer.name)
        history.save()
        untappd_checkout = request.POST.get("untappdCheckout", "")
        untappd_rating = request.POST.get("untappdRating", "")
        if untappd_checkout:
            member = MemberTable.objects.get(user=request.user)

            api = pythonUntappd.api(settings.UNTAPPD_CLIENT_ID, settings.UNTAPPD_CLIENT_SECRET)
            api.set_auth(member.untappdAuth)

            untappd_response = api.checkin('-8', 'PST', bid, rating=untappd_rating)

            if untappd_response['meta']['code'] == 500:
                failure = json.dumps(untappd_response, sort_keys=True, indent=4, separators=(',', ': '))
                context = Context({
                    'user': request.user,
                    'response': failure,
                })
                return render(request, 'beers/failed.html', context)
        context = Context({
            'name': beer.name,
            'amount': stock.amountDrank,
            'left': stock.amountInStock,
            'user': request.user,
        })
        return render(request, 'beers/success.html', context)
    else:
        context = Context({
            'beer': beer,
            'stock': stock,
            'user': request.user,
        })
        return render(request, 'beers/untappd_beer_checkout.html', context)
