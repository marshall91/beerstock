# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from beers.models import Beer, Brewery, Type, BeerForm, BreweryForm, TypeForm

@login_required
def stock_index(request):
	all_beer_list = Beer.objects.filter(owner=request.user, amountInFridge__gt=0)
	template = loader.get_template('beers/stock_index.html')
	context = Context({
		'all_beer_list': all_beer_list,
		'user' : request.user,
	})
	return HttpResponse(template.render(context))

@login_required	
def beer_index(request):
	all_beer_list = Beer.objects.filter(owner=request.user, amountConsumed__gt=0)
	template = loader.get_template('beers/beer_index.html')
	context = Context({
		'all_beer_list': all_beer_list,
		'user' : request.user,
	})
	return HttpResponse(template.render(context))

@login_required	
def brewery_index(request):
	all_brewery_list = Brewery.objects.all()
	template = loader.get_template('beers/brewery_index.html')
	context = Context({
		'all_brewery_list': all_brewery_list,
		'user' : request.user,
	})
	return HttpResponse(template.render(context))

@login_required
def beer_type_index(request):
	all_beer_type_list = Type.objects.all()
	template = loader.get_template('beers/beer_type_index.html')
	context = Context({
		'all_beer_type_list': all_beer_type_list,
		'user' : request.user,
	})
	return HttpResponse(template.render(context))

@login_required	
def beer_detail(request, beer_name):
	try:
		beer = Beer.objects.get(name=beer_name, owner=request.user)
		if request.method == "POST":
			beer.amountConsumed = beer.amountConsumed + 1
			beer.amountInFridge = beer.amountInFridge - 1
			beer.save()
			return render_to_response('beers/success.html')
		else:
			template = loader.get_template('beers/beer_info.html')
			context = Context({
				'beer' : beer,
				'user' : request.user,
			})
			return render_to_response('beers/beer_info.html', context, RequestContext(request))
	except ObjectDoesNotExist:
		beer = Beer.objects.get(name=beer_name)
		beer.amountConsumed = 0
		beer.amountInFridge = 0
		template = loader.get_template('beers/beer_info.html')
		context = Context({
			'beer' : beer,
			'user' : request.user,
		})
		return render_to_response('beers/beer_info.html', context, RequestContext(request))

@login_required
def brewery_detail(request, brewery_name):
	brewery = Brewery.objects.get(name=brewery_name)
	beer_list = Beer.objects.filter(brewery=brewery.id).values('name','brewery__name','beerType__name').distinct()
	template = loader.get_template('beers/brewery_info.html')
	context = Context({
		'brewery' : brewery,
		'beer_list' : beer_list,
		'user' : request.user,
	})
	return HttpResponse(template.render(context))

@login_required	
def beer_type_detail(request, beer_type_name):
	beer_type = Type.objects.get(name=beer_type_name)
	beer_list = Beer.objects.filter(beerType=beer_type.id).values('name','brewery__name','beerType__name').distinct()
	template = loader.get_template('beers/beer_type_info.html')
	context = Context({
		'beer_type' : beer_type,
		'beer_list' : beer_list,
		'user' : request.user,
	})
	return HttpResponse(template.render(context))	
	
def logged_out(request):
	return render_to_response('beers/logout_success.html')
	
@login_required
def add_new_beer(request):
	if request.method == "POST":
		user = request.user
		beer = Beer(owner=user)
		form = BeerForm(request.POST,instance=beer)
		new_beer = form.save()
		return render_to_response('beers/success.html')
	else:
		formset = BeerForm()
		context = Context({
			'formset' : formset,
		})
		return render_to_response('beers/beer_form.html', context, RequestContext(request))

@login_required
def add_new_brewery(request):
	if request.method == "POST":
		brewery = Brewery(uniqueBeers=0)
		form = BreweryForm(request.POST,instance=brewery)
		new_brewery = form.save()
		return render_to_response('beers/success.html')
	else:
		formset = BreweryForm()
		context = Context({
			'formset' : formset,
		})
		return render_to_response('beers/brewery_form.html', context, RequestContext(request))
		
@login_required
def add_new_type(request):
	if request.method == "POST":
		type = Type()
		form = TypeForm(request.POST,instance=type)
		new_type = form.save()
		return render_to_response('beers/success.html')
	else:
		formset = TypeForm()
		context = Context({
			'formset' : formset,
		})
		return render_to_response('beers/beer_type_form.html', context, RequestContext(request))
		