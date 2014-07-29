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

from beers.models import MemberTable
from forms import UserForm
from Untappd import UntappdGetAuthToken


def account_info(request):
    context = Context({
        'CLIENTID': settings.UNTAPPD_CLIENT_ID,
        'REDIRECT_URL': "http://www.beerstock.ca/account/account_auth",
        'user': request.user,
    })
    return render(request, 'account/account_info.html', context)


def account_update(request):
    code = request.GET.get('code')
    token = UntappdGetAuthToken(code)
    try:
        member = MemberTable.objects.get(user=request.user.id)
    except ObjectDoesNotExist:
        member = MemberTable(user=request.user.id)
    member.untappdAuth = token
    member.save()
    context = Context({
        'user': request.user,
    })
    return render(request, 'beers/success.html', context)


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect('/beers/stock_index')
    else:
        form = UserForm()

    return render(request, 'account/signup.html', {'form': form})


def logged_out(request):
    return render(request, 'account/logout_success.html')
