from beers.models import BeerTable
from django.conf import settings
import httplib, urllib, urllib2, json
from django.core.exceptions import ObjectDoesNotExist

def UntappdGetAuthToken(code):
    params = urllib.urlencode({'client_id': settings.UNTAPPD_CLIENT_ID, 'client_secret': settings.UNTAPPD_CLIENT_SECRET,
                               'response_type': 'code', 'redirect_url': "http://www.beerstock.ca/account/account_auth",
                               'code': code})
    conn = httplib.HTTPSConnection("untappd.com")
    conn.request("GET", "/oauth/authorize/?"+params)
    response = conn.getresponse()
    json_response = json.loads(response.read())
    conn.close()
    if json_response['meta']['http_code'] == 200:
        token = json_response['response']['access_token']
    else:
        token = "null"

    return token

