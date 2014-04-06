from beers.models import BeerTable
from django.conf import settings
import httplib, urllib, urllib2, json
from django.core.exceptions import ObjectDoesNotExist

UNTAPPD_CLIENT_ID = "CF9D45955B760732A44FE2E836228BF53AC26763"
UNTAPPD_CLIENT_SECRET = "805F76302BD227868AF94F897EE041E82E4DE611"


def UntappdSearch(query):
    params = urllib.urlencode({'client_id': UNTAPPD_CLIENT_ID, 'client_secret': UNTAPPD_CLIENT_SECRET, 'q': query, 'sort': 'count'})
    conn = httplib.HTTPConnection("api.untappd.com")
    conn.request("GET", "/v4/search/beer?"+params)
    response = conn.getresponse()
    json_response = json.loads(response.read())
    conn.close()

    return json_response


def UntappdCheckout(auth, bid):
    params = urllib.urlencode({'gmt_offset': -8, 'timezone': 'PST', 'bid': bid})
    url = "http://api.untappd.com/v4/checkin/add?access_token="+auth
    response = urllib2.urlopen(url, params).read()
    json_response = json.loads(response)

    return json_response


def UntappdGetAuthToken(code):
    params = urllib.urlencode({'client_id': UNTAPPD_CLIENT_ID, 'client_secret': UNTAPPD_CLIENT_SECRET,
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


def GetUntappdClientId():
    return UNTAPPD_CLIENT_ID


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

