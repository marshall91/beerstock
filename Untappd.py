from beers.models import BeerTable
from django.conf import settings
import httplib, urllib, urllib2, json

UNTAPPD_CLIENT_ID = "CF9D45955B760732A44FE2E836228BF53AC26763"
UNTAPPD_CLIENT_SECRET = "805F76302BD227868AF94F897EE041E82E4DE611"


def UntappdSearch(query):
	params = urllib.urlencode({'client_id': UNTAPPD_CLIENT_ID, 'client_secret': UNTAPPD_CLIENT_SECRET, 'q': query, 'sort': 'count'}) 
	conn = httplib.HTTPConnection("api.untappd.com")
	conn.request("GET", "/v4/search/beer?"+params)
	response = conn.getresponse() 
	jsonResponse = json.loads(response.read())
	conn.close()

	return jsonResponse

def UntappdCheckout(auth, bid):
	params = urllib.urlencode({'gmt_offset': -8, 'timezone': 'PST', 'bid': bid})
	url = "http://api.untappd.com/v4/checkin/add?access_token="+auth
	response = urllib2.urlopen(url, params).read()
	jsonResponse = json.loads(response)

	return jsonResponse

def UntappdGetAuthToken(code):
	params = urllib.urlencode({'client_id': UNTAPPD_CLIENT_ID, 'client_secret': UNTAPPD_CLIENT_SECRET, 'reponse_type': 'code', 'redirect_url' : "http://www.beerstock.ca/beers/account_auth", 'code': code}) 
	conn = httplib.HTTPSConnection("untappd.com")
	conn.request("GET", "/oauth/authorize/?"+params)
	response = conn.getresponse() 
	jsonResponse = json.loads(response.read())
	conn.close()
	if jsonResponse['meta']['http_code'] == 200:
		token = jsonResponse['response']['access_token']
	else:
		token = "null"

	return token

def GetUntappdClientId():
	return UNTAPPD_CLIENT_ID

def JsonToBeer(entry):
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

	return newBeer

