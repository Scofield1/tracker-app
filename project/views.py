from django.shortcuts import render
import phonenumbers, folium
from phonenumbers import geocoder, carrier, timezone
from opencage.geocoder import OpenCageGeocode
key = '35812db4437a4de6a264f433d4438400'


def index(request):
    return render(request, 'index.html', {})


def result(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        get_number = phonenumbers.parse(number)
        location = geocoder.description_for_number(get_number, 'en')
        np = carrier.name_for_number(get_number, 'en')
        timeZone = timezone.time_zones_for_number(get_number)
        geo_key = OpenCageGeocode(key)
        query = str(location)
        results = geo_key.geocode(query)
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        my_map = folium.Map(location=[lat, lng], zoom_start=9,)
        marker = folium.Marker([lat, lng], popup=location)
        marker.add_to(my_map)
        my_map.save('templates/location.html')
        context = {'location': location, 'np': np, 'number': number, 'lat': results[0]['geometry']['lat'],
                   'lng': results[0]['geometry']['lng'], 'my_map': my_map,
                   'time': timeZone,}
    return render(request, 'results.html', context)


def location(request):
    return render(request, 'location.html', {})