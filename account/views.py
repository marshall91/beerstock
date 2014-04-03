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

from beers.models import MemberTable
from forms import UserForm
from Untappd import *


def account_info(request):
    template = loader.get_template('account/account_info.html')
    context = Context({
        'CLIENTID': GetUntappdClientId(),
        'REDIRECT_URL': "http://www.beerstock.ca/account/account_auth",
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def account_update(request):
    code = request.GET.get('code')
    token = UntappdGetAuthToken(code)
    try:
        member = MemberTable.objects.get(user=request.user)
    except ObjectDoesNotExist:
        member = MemberTable(user=request.user)
    member.untappdAuth = token
    member.save()
    context = Context({
        'user': request.user,
    })
    return render_to_response('beers/success.html', context)


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return HttpResponseRedirect('/beers/stock_index')
    else:
        form = UserForm()

    return render(request, 'account/signup.html', {'form': form})