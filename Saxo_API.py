from saxo_openapi import API
import saxo_openapi.endpoints.trading as tr
import saxo_openapi.endpoints.portfolio as pf
from saxo_openapi.contrib.orders import tie_account_to_order, MarketOrderFxSpot
from saxo_openapi.contrib.session import account_info
import json

user_id_SAXO = 13619172
user_token = 'eyJhbGciOiJFUzI1NiIsIng1dCI6IjhGQzE5Qjc0MzFCNjNFNTVCNjc0M0QwQTc5MjMzNjZCREZGOEI4NTAifQ.eyJvYWEiOiI3Nzc3NSIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiVXB1aVVycUU1cXR2QlRGT2lSVHJhQT09IiwiY2lkIjoiVXB1aVVycUU1cXR2QlRGT2lSVHJhQT09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiOTUzOTFiYWFmN2MwNDg0MGJjNDQzMTJiOWE1MmFmMWYiLCJkZ2kiOiI4NCIsImV4cCI6IjE2MTQ3MTQ2NzYifQ.gT09t2XS-sCs6E-Ou3f7_e9h8Xnqf4Wdhj8rhtXXIIDogSRKS_nUc7N08z-cW1itkGlIoY_LxGLU6UwrCDLZFw'

endpoints_documentation = 'https://saxo-openapi.readthedocs.io/en/latest/'
saxo_api_documentation = 'https://saxo-openapi.readthedocs.io/_/downloads/en/latest/pdf/'

from saxo_openapi import API
from saxo_openapi.contrib.orders import tie_account_to_order, LimitOrderStock
import saxo_openapi.endpoints.trading as tr

client = API(access_token=user_token)
order = tie_account_to_order(
    AccountKey,
    LimitOrderStock(Uic=16350, Amount=1000, OrderPrice=28.00))
r = tr.orders.Order(data=order)
rv = client.request(r)
print(json.dumps(rv, indent=2))

import saxo_openapi
import saxo_openapi.endpoints.accounthistory as ah
import json
client = saxo_openapi.API(access_token=...)
ClientKey = 'Cf4xZWiYL6W1nMKpygBLLA=='
r = ah.accountvalues.AccountSummary(ClientKey=ClientKey)
client.request(r)
print(json.dumps(r.response, indent=2))

#get charting data

import saxo_openapi.endpoints.chart as ch
import json
client = saxo_openapi.API(access_token=user_token)
data ={
  "Arguments": {
            "AssetType": "FxSpot",
            "Count": 2,
            "Horizon": 1,
            "Uic": 21
          },
          "ContextId": "20190830035501020",
          "Format": "application/json",
          "ReferenceId": "UIC_21",
          "RefreshRate": 1000
}

r = ch.charts.CreateChartDataSubscription(data=data)
client.request(r)
print(json.dumps(rv, indent=2))

import saxo_openapi.endpoints.chart as chart
import json
client = saxo_openapi.API(access_token=...)
params ={
      "AssetType": "FxSpot",
      "Horizon": 60,
      "Count": 24,
      "Uic": 23
}

r = chart.charts.GetChartData(params=params)
client.request(r)
print(json.dumps(rv, indent=2))