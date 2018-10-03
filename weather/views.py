from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url ='http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=<YOUR KEY>'
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    weather_data = []

    cities = City.objects.all()

    for city in cities:
        r = requests.get(url.format(city)).json()
        if str(r['cod']) == str(404):
            print('Not Found')
        else:
            city_weather = {
            'city':city.name,
            'temperature': r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon']
            }
            weather_data.append(city_weather)
    context = {'weather_data':weather_data, 'form':form}
    return render(request, 'weather/weather.html', context)
