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

import httplib, urllib, json

clientId = "CF9D45955B760732A44FE2E836228BF53AC26763"
clientSecret = "805F76302BD227868AF94F897EE041E82E4DE611"
	
def logged_out(request):
	return render_to_response('beers/logout_success.html')
		
@login_required
def search_beer(request):
	if request.method == "POST":
		beer = request.POST.get("beername", "")
		params = urllib.urlencode({'client_id': clientId, 'client_secret': clientSecret, 'q': beer, 'sort': 'count'}) 
		conn = httplib.HTTPConnection("api.untappd.com")
		conn.request("GET", "/v4/search/beer?"+params)
		response = conn.getresponse() 
		jsonResponse = json.loads(response.read())
		conn.close()
		
		if jsonResponse['meta']['code'] == 200:
			beer_list = []
			for entry in jsonResponse['response']['beers']['items']:
				newBeer = BeerTable()
				newBeer.untappdId = entry['beer']['bid']
				newBeer.name = entry['beer']['beer_name']
				newBeer.style = entry['beer']['beer_style']
				newBeer.imgUrl = entry['beer']['beer_label']
				newBeer.abv = entry['beer']['beer_abv']
				newBeer.breweryName = entry['brewery']['brewery_name']
				newBeer.breweryId = entry['brewery']['brewery_id']
				try:
					dbBeer = BeerTable.objects.get(untappdId=newBeer.untappdId)	
				except ObjectDoesNotExist:
					newBeer.save()
				dbBeer = BeerTable.objects.get(untappdId=newBeer.untappdId)
				newBeer.id = dbBeer.id
				beer_list.append(newBeer)
			
			for entry in jsonResponse['response']['homebrew']['items']:
				newBeer = BeerTable()
				newBeer.untappdId = entry['beer']['bid']
				newBeer.name = entry['beer']['beer_name']
				newBeer.style = entry['beer']['beer_style']
				newBeer.imgUrl = entry['beer']['beer_label']
				newBeer.abv = entry['beer']['beer_abv']
				newBeer.breweryName = entry['brewery']['brewery_name']
				newBeer.breweryId = entry['brewery']['brewery_id']
				try:
					dbBeer = BeerTable.objects.get(untappdId=newBeer.untappdId)	
				except ObjectDoesNotExist:
					newBeer.save()
				dbBeer = BeerTable.objects.get(untappdId=newBeer.untappdId)
				newBeer.id = dbBeer.id
				beer_list.append(newBeer)
				
			context = Context({
				'beer_list': beer_list,
				'user' : request.user,
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
		newHistory = request.POST.get("history", "")
		newStock = request.POST.get("stock", "")
		try:
			stock = StockTable.objects.get(untappdId=beer.untappdId, owner=user)
		except ObjectDoesNotExist:
			stock = StockTable(amountDrank=0,amountInStock=0, owner=user, untappdId=beer.untappdId)
		stock.beerName = beer.name
		stock.amountDrank = newHistory
		stock.amountInStock = newStock
		stock.save()
		context = Context({
			'user' : request.user,
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
		'user' : request.user,
	})
	return HttpResponse(template.render(context))
	
@login_required
def history_index(request):
	all_beer_list = HistoryTable.objects.filter(owner=request.user).order_by('-timestamp')
	template = loader.get_template('beers/history_index.html')
	context = Context({
		'all_beer_list': all_beer_list,
		'user' : request.user,
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
		untappdCheckout = request.POST.get("untappdCheckout", "")
		print untappdCheckout
		if(untappdCheckout):
			member = MemberTable.objects.get(user=request.user)
			params = urllib.urlencode({'access_token': member.untappdAuth, 'gmt_offset': member.gmtOffset, 'timezone': member.timezone, 'bid': bid}) 
			conn = httplib.HTTPConnection("api.untappd.com")
			conn.request("POST", "/v4/checkin/add?"+params)
			response = conn.getresponse() 
			jsonResponse = json.loads(response.read())
			conn.close()
			
		context = Context({
			'user' : request.user,
		})
		return render_to_response('beers/success.html', context)
	else:
		context = Context({
			'beer': beer,
			'stock': stock,
			'user': request.user,
		})
		return render_to_response('beers/untappd_beer_checkout.html', context, RequestContext(request))
		
def account_info(request):
	template = loader.get_template('beers/account_info.html')
	context = Context({
		'CLIENTID' : clientId,
		'REDIRECT_URL' : "http://www.beerstock.ca/beers/account_auth",
		'user' : request.user,
	})
	return HttpResponse(template.render(context))
	
def account_update(request):
	code = request.GET.get('code')
	params = urllib.urlencode({'client_id': clientId, 'client_secret': clientSecret, 'reponse_type': 'code', 'redirect_url' : "http://www.beerstock.ca/beers/account_auth", 'code': code}) 
	conn = httplib.HTTPConnection("https://untappd.com")
	conn.request("GET", "/oauth/authorize/?"+params)
	response = conn.getresponse() 
	jsonResponse = json.loads(response.read())
	conn.close()
	if jsonResponse['meta']['code'] == 200:
		token = jsonResponse['response']['access_token']
	else:
		token = "null"
	try:
		member = MemberTable.objects.get(user=request.user)
	except ObjectDoesNotExist:
		member = MemberTable(user=request.user)
	member.untappdAuth = token
	member.save()
	context = Context({
		'user' : request.user,
	})
	return render_to_response('beers/success.html', context)
	