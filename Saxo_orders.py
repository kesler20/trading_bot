from saxo_openapi import API
import saxo_openapi.endpoints.trading as tr
import saxo_openapi.endpoints.portfolio as pf
import json

# Place your token in a file named: tok.txt
tok = ""
with open("tok.txt") as I:
    tok = I.read().strip()

# Our client to process the requests
client = API(access_token=tok)

# Place some market orders
MO = [
{
    "AccountKey": "Cf4xZWiYL6W1nMKpygBLLA==",
    "Amount": "100000",
    "AssetType": "FxSpot",
    "BuySell": "Sell",
    "OrderType": "Market",
    "Uic": 21   # EURUSD
},
{
    "AccountKey": "Cf4xZWiYL6W1nMKpygBLLA==",
    "Amount": "80000",
    "AssetType": "FxSpot",
    "BuySell": "Buy",
    "OrderType": "Market",
    "Uic": 23   # GBPCAD
},
]

# create Order requests and process them
for r in [tr.orders.Order(data=orderspec) for orderspec in MO]:
    client.request(r)

