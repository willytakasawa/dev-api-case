from urllib import response
import requests

URL = "http://localhost:5000/"

try:
    response = requests.get(URL + "cancelamento")
    print(response.json())

except Exception as e:
    print(e)