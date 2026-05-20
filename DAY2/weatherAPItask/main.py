import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.20&current_weather=true"

response = requests.get(url)

data = response.json()

weather = data["current_weather"]

temperature = weather["temperature"]
windspeed = weather["windspeed"]

print(f"Temperature: {temperature}°C")
print(f"Wind Speed: {windspeed} km/h")