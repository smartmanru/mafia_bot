import urllib.parse
import requests
def geocoder(geocode:str):
    geo=urllib.parse.quote(geocode)
    r=requests.get('https://geocode-maps.yandex.ru/1.x/?apikey=b602cecc-4702-405d-b23c-04650c6a1d75&geocode=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0,+'+geo+'&format=json&results=1')
    a=r.json()
    return(a['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'])