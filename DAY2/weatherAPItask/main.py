import requests       
import json           # save report to file
import asyncio        # to run async function
import httpx          # for async API calls
import os             # to read env var
from datetime import datetime      # for timestamp in report
from dotenv import load_dotenv     
from pydantic import BaseModel     # validation of data which comes from api

class WeatherData(BaseModel):  # this pydantic validation appling
    city: str
    temp: float
    humidity : int
    desc: str
    windspeed : float


load_dotenv()  
api_key = os.getenv("Weather_apiKey")

# city = "Jaipur"
cities = ["Delhi", "Jaipur", "Kolkata", "Mumbai"]

async def fetch_weatherData(city):
    async with httpx.AsyncClient() as weatherClient:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        
        # response = await weatherClient.get(url) 
        # right now this run only one time mean may it fail so i apply try fail block
        #appling try block if failed case

        for attempt in range(3): # it will run only for 3 times 
            try:
                response = await weatherClient.get(url)
                if response.status_code == 200:
                    break

                elif response.status_code == 429:
                    print(f"rate limit hit  for {city}.. retry pls..")
                    await asyncio.sleep(3)
                
                else :
                    print(f"retrying for city..{city} ... attempt {attempt+1}")
                    await asyncio.sleep(2)


            except Exception as e :
                print(f"Error in {city} : {e}")


        data = response.json()

        if response.status_code != 200:
            print(f"{city} is not found")
            return
        
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"]
        windspeed = data["wind"]["speed"]



        
        validate_weather = WeatherData(
            city = city,
            temp = temperature,
            humidity = humidity,
            desc = desc,
            windspeed = windspeed
        )

        

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        weather_report = {
            "city": validate_weather.city,
            "temperature" : validate_weather.temp,
            "humidity" : validate_weather.humidity,
            "description" : validate_weather.desc,
            "windspeed" : validate_weather.windspeed,
            "timestamp" : timestamp
        }

        # with open("weather_report.json", "a") as file:   for everytime creating new file for every new city in this case
        #     json.dump(weather_report , file, indent=4)

        with open("weather_report.json", "a") as file:    # now for all city data save in only one file
            file.write(json.dumps(weather_report, indent=4))
            file.write("\n")

            
        print(f"{city} weather save successfuly!")


async def main():

    tasks = []

    for city in cities:
        tasks.append(fetch_weatherData(city))

    await asyncio.gather(*tasks)

asyncio.run(main())
   



#Sync code practisee

# url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

# response = requests.get(url)
# data = response.json() #json data into python dic formate me 
# #print(data) iss se ye check kro data ka formate kis me ky hai then initialized in profesional way
# temperature = data["main"]["temp"]
# humidity = data["main"]["humidity"]
# desc = data["weather"][0]["description"]
# windspeed = data["wind"]["speed"]

 
# validate_weather = WeatherData(
#     city = city,
#     temp = temperature,
#     humidity=humidity,
#     desc =  desc,
#     windspeed=windspeed
# )
# timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # this validate the timestamp of weather

# weather_report ={
#     "city" :validate_weather.city,
#     "temprature": validate_weather.temp,
#     "humidity": validate_weather.humidity,
#     "windspeed": validate_weather.windspeed,
#     "description" : validate_weather.desc,
#     "timestamp": timestamp
# }

# #now save this data in json wile
# with open("weather_report.json", "w") as file :
#     json.dump(weather_report, file, indent=4)

# print("weather report save DONEEE")

# print(f"city: {city}")
# print(f"temp: {temperature}")
# print(f"humidity : {humidity}")
# print(f"weather : {desc}")
# print(f"windspeed: {windspeed}")



async def fetch_weatherData(city):
    async with httpx.AsyncClient() as weatherClient:   # AsyncClient() is library in httpx
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = await weatherClient.get(url)
        data = response.json()
        print(city, data["main"]["temp"])



asyncio.run(fetch_weatherData("Delhi"))















# url = "https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.20&current_weather=true"

# response = requests.get(url)

# data = response.json()

# weather = data["current_weather"]

# validated_weather = weatherData(
    
# )
# temperature = weather["temperature"]
# windspeed = weather["windspeed"]

# print(f"Temperature: {temperature}°C")
# print(f"Wind Speed: {windspeed} km/h")


# with open("weather_report.txt", "w") as file:
#     file.write(
#         f"Temperature: {validated_weather.temperature}°C\n"
#         f"Wind Speed: {validated_weather.windspeed} km/h"
#     )