# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from beers.models import BeerTable, StockTable, HistoryTable, MemberTable
from Untappd import *

import json


@login_required
def search_beer(request):
    if request.method == "POST":
        beer = request.POST.get("beername", "")

        untappd_response = UntappdSearch(beer)

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
            return render_to_response('beers/beer_list.html', context, RequestContext(request))
    else:
        context = Context({
        })
        return render_to_response('beers/untappd_beer_form.html', context, RequestContext(request))


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
        context = Context({
            'user': request.user,
        })
        return render_to_response('beers/success.html', context)
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
        return render_to_response('beers/untappd_beer_update.html', context, RequestContext(request))


@login_required
def stock_index(request):
    all_beer_list = StockTable.objects.filter(owner=request.user, amountInStock__gt=0)
    template = loader.get_template('beers/stock_index.html')
    context = Context({
        'all_beer_list': all_beer_list,
        'user': request.user,
    })
    return HttpResponse(template.render(context))


@login_required
def history_index(request):
    all_beer_list = HistoryTable.objects.filter(owner=request.user).order_by('-timestamp')
    template = loader.get_template('beers/history_index.html')
    context = Context({
        'all_beer_list': all_beer_list,
        'user': request.user,
    })
    return HttpResponse(template.render(context))


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
        if untappd_checkout:
            member = MemberTable.objects.get(user=request.user)
            untappd_response = UntappdCheckout(member.untappdAuth, bid)
            if untappd_response['meta']['code'] == 500:
                failure = json.dumps(untappdResponse, sort_keys=True, indent=4, separators=(',', ': '))
                context = Context({
                    'user': request.user,
                    'response': failure,
                })
                return render_to_response('beers/failed.html', context)
        context = Context({
            'user': request.user,
        })
        return render_to_response('beers/success.html', context)
    else:
        context = Context({
            'beer': beer,
            'stock': stock,
            'user': request.user,
        })
        return render_to_response('beers/untappd_beer_checkout.html', context, RequestContext(request))
