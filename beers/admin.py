from django.contrib import admin
from beers.models import BeerTable, StockTable, HistoryTable

admin.site.register(BeerTable)
admin.site.register(StockTable)
admin.site.register(HistoryTable)