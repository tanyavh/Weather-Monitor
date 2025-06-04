#use this script to test your api key 

import requests

API_KEY = 'insert_api_key'
CITY = 'city_name'
UNITS = 'metric'

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"
response = requests.get(url)
print(response.status_code)
print(response.text)
