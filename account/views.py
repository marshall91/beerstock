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


@login_required
def account_settings(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        if request.POST['new_password'] != '':
            user.set_password(request.POST['new_password'])
        user.save()
        try:
            member_extra = MemberTable.objects.get(user=user)
        except ObjectDoesNotExist:
            member_extra = MemberTable(user=user)

        context = Context({
            'CLIENTID': settings.UNTAPPD_CLIENT_ID,
            'REDIRECT_URL': "http://www.beerstock.ca/account/account_auth",
            'user': user,
            'member_extra': member_extra,
            })
        return render(request, 'account/account_settings.html', context)
    else:
        user = request.user
        try:
            member_extra = MemberTable.objects.get(user=user)
        except ObjectDoesNotExist:
            member_extra = MemberTable(user=user)

        context = Context({
            'CLIENTID': settings.UNTAPPD_CLIENT_ID,
            'REDIRECT_URL': "http://www.beerstock.ca/account/account_auth",
            'user': request.user,
            'member_extra': member_extra,
        })
        return render(request, 'account/account_settings.html', context)


@login_required
def account_update(request):
    code = request.GET.get('code')
    token = UntappdGetAuthToken(code)
    user = User.objects.get(id=request.user.id)
    try:
        member = MemberTable.objects.get(user=user)
    except ObjectDoesNotExist:
        member = MemberTable(user=user)
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
