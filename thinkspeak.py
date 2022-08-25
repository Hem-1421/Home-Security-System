from urllib.request import urlopen
import sys

WRITE_API = "WXH40ZF14XYYB0VH" # Replace your ThingSpeak API key here
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)
 



thingspeakHttp = BASE_URL + "&field3=free"
print(thingspeakHttp)

conn = urlopen(thingspeakHttp)
print("Response: {}".format(conn.read()))
conn.close()

