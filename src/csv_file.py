import http.client
import csv
import json
import os.path
from os import path
import numpy as np
from datetime import date
import time
ts = time.time()
# print(int(ts))

symbol = "ABBV"

conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "ba96fccb1cmsh76bbff0c1275b81p1c6cf4jsn1b36b51d2cd4"
    }

conn.request("GET", "/stock/v2/get-historical-data?frequency=1d&filter=history&period1=0&period2=" + str(int(ts)) + "&symbol=" + symbol, headers=headers)

res = conn.getresponse()
data = res.read()
new_str = data.decode("utf-8")

# Get data string length
length = len(new_str)
print("\n>> string_length " + str(length) + "\n")

# Parse each object
json_data = new_str[0:length].replace("},", "},\n")
# print(json_data)

# json result
res = json.loads(json_data)

# sets prices key
prices = res['prices']
print(type(prices))
myarray = np.asarray(prices)
myarray_length = len(myarray)

new_list = []

for i in range(1, myarray_length):
    my_str = myarray[i]
    if "type" not in my_str:
        new_list.append(my_str)
    continue

prices = new_list

price_length = len(prices)
print(">> price_length " + str(price_length) + "\n")
price_date = []
price_open = []
price_close = []
price_high = []
price_low = []
price_volume = []
price_adjclose = []

# push data on to their rows
try:
    for price_data in prices:
        price_date.append(price_data['date'])
        price_open.append(price_data['open'])
        price_close.append(price_data['close'])
        price_high.append(price_data['high'])
        price_low.append(price_data['low'])
        price_volume.append(price_data['volume'])
        price_adjclose.append(price_data['adjclose'])
        
        # print("price_date_" + str(price_date))
        # print("price_open_" + str(price_open))
        # print("price_close_" + str(price_close))
        # print("price_high_" + str(price_high))
        # print("price_low_" + str(price_low))
        # print("price_volume_" + str(price_volume))
        # print("price_adjclose_"+ str(price_adjclose) + "\n")
except KeyError:
    print('>> No more rows to append\n')

# Check the size of strenght length
if length > 100000000:
    print(">> More data has been added to string\n")
else:
    new_str = new_str[0:21380].replace("{", "")
    new_str = new_str[0:21380].replace("}", "")
    new_str = new_str[0:21380].replace("[", "")
    new_str = new_str[0:21380].replace("]", "")
    new_str = new_str[0:21380].replace('"', "")
    new_str = new_str[0:21380].replace(",", ",\n")
    new_str = new_str[0:21380].replace("prices:", "")
    new_str = new_str[0:21380].replace("''", "")
    # print(new_str)

	# Assigns key fields names
    fieldnames = ["date", "open", "high", "low", "close", "volume", "adjclose"]

    if path.exists("../csv/" + symbol + ".timeseries.csv") == True:
        with open("../csv/" + symbol + '.timeseries.csv', 'a', newline='') as file:
			# Tell the writer what he labels are
            writer = csv.DictWriter(file, fieldnames=fieldnames)
			# For each price date in prices
            for i in range(1, price_length):
                writer.writerow({"date" : price_date[i], "open" : price_open[i], "high" : price_high[i], "low" : price_low[i], "close" : price_close[i], "volume" : price_volume[i], "adjclose" : price_adjclose[i]})
    else:
        with open("../csv/" + symbol + '.timeseries.csv', 'w', newline='') as file:
			# Tell the writer what he labels are
            writer = csv.DictWriter(file, fieldnames=fieldnames)
			# Distribute Labels
            writer.writeheader()	
			# For each price date in prices
            for i in range(1, price_length):
                writer.writerow({"date" : date.fromtimestam p(price_date[i]), "open" : price_open[i], "high" : price_high[i], "low" : price_low[i], "close" : price_close[i], "volume" : price_volume[i], "adjclose" : price_adjclose[i]})