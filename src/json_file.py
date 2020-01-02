import http.client
import csv
import json
import numpy as np

conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "ba96fccb1cmsh76bbff0c1275b81p1c6cf4jsn1b36b51d2cd4"
    }

conn.request("GET", "/stock/v2/get-historical-data?frequency=1d&filter=history&period1=1514795400&period2=1562086800&symbol=IBM", headers=headers)

res = conn.getresponse()
data = res.read()
new_str = data.decode("utf-8")

# Get data string length
length = len(new_str)
print("\n>> string_length " + str(length) + "\n")

# Parse each object
new_str = new_str[0:length].replace("},", "},\n")
# print(new_str)

# json result
res = json.loads(new_str)

# sets prices key
prices = res['prices']
print(type(prices))
# print(prices)

myarray = np.asarray(prices)
myarray_length =len(myarray)

for i in range(1, myarray_length):
    my_str = str(i) + " " + str(myarray[i])
    if "type" not in my_str:
        print(my_str)
    continue

price_length = len(prices)
price_date = []
price_open = []
price_close = []
price_high = []
price_low = []
price_volume = []
price_adjclose = []

# loops over price LIST
try:
    for price_data in prices:
        price_date.append(price_data['date'])
        price_open.append(price_data['open'])
        price_close.append(price_data['close'])
        price_high.append(price_data['high'])
        price_low.append(price_data['low'])
        price_volume.append(price_data['volume'])
        price_adjclose.append(price_data['adjclose'])
        
        # print("price_open_" + str(price_date) + " " + str(price_open))
        # print("price_close_" + str(price_date) + " " + str(price_close))
        # print("price_high_" + str(price_date) + " " + str(price_high))
        # print("price_low_" + str(price_date) + " " + str(price_low))
        # print("price_volume_" + str(price_date) + " " + str(price_volume))
        # print("price_adjclose_" + str(price_date) + " " + str(price_adjclose) + "\n")
except KeyError:
    print('ERROR: key not found')
    