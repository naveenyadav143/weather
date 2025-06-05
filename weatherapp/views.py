from django.shortcuts import render
import json
import urllib.request

def index(request):
    if request.method == "POST":
        city = request.POST.get("city", "").strip()
        if not city:
            return render(request, 'index.html', {'error': 'Please enter a city name.'})

        try:
            api_key = "ca8d9f88b055498998f42825250506"   # replace this with your actual WeatherAPI key
            api_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1"

            response = urllib.request.urlopen(api_url).read()
            json_data = json.loads(response)

            data = {
                "city": json_data["location"]["name"],
                "country": json_data["location"]["country"],
                "temp": json_data["current"]["temp_c"],
                "condition": json_data["current"]["condition"]["text"],
                "icon": json_data["current"]["condition"]["icon"],
                "humidity": json_data["current"]["humidity"],
                "wind_kph": json_data["current"]["wind_kph"],
            }

            # Get rain forecast (precipitation in mm for today)
            rain = None
            rain_chance = None
            if "forecast" in json_data and "forecastday" in json_data["forecast"] and len(json_data["forecast"]["forecastday"]) > 0:
                rain = json_data["forecast"]["forecastday"][0]["day"].get("daily_will_it_rain", 0)
                rain_mm = json_data["forecast"]["forecastday"][0]["day"].get("totalprecip_mm", 0)
                rain_chance = json_data["forecast"]["forecastday"][0]["day"].get("daily_chance_of_rain", 0)
            else:
                rain = 0
                rain_mm = 0
                rain_chance = 0

            weather_str = (
                f"Weather in {data['city']}, {data['country']}: "
                f"{data['condition']}, {data['temp']}°C, "
                f"Humidity: {data['humidity']}%, Wind: {data['wind_kph']} kph, "
                f"Rain: {'Yes' if rain else 'No'}, Precipitation: {rain_mm} mm, "
                f"Chance of Rain: {rain_chance}%"
            )

            return render(request, 'index.html', {
                'city': data['city'],
                'temp': data['temp'],
                'condition': data['condition'],
                'humidity': data['humidity'],
                'wind_kph': data['wind_kph'],
                'icon': data['icon'],
                'weather_str': weather_str,
                'rain': rain,
                'rain_mm': rain_mm,
                'rain_chance': rain_chance,
            })

        except Exception as e:
            return render(request, 'index.html', {'error': f"Could not retrieve weather data. ({str(e)})"})

    return render(request, 'index.html')
