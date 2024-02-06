import requests, os
from twilio.rest import Client

# Env Var needed:
# api_KEY
# account_SID
# auth_TOKEN

#------------------ START OF WEATHER VARIABLE SETUP ------------------------ #

api_key = os.environ.get('API_KEY')    #the API Key from the open weather website
print(f"The api key is: {api_key}")

# FULL_URL = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&api_key={API key}"
# API_Weather_URL_Endpoint = "https://api.openweathermap.org/data/2.5/weather"

API_Weather_URL_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# BUT for the 5 DAY forecast with 3 hour interval updates, it is this URL:
# https://openweathermap.org/forecast5

updated_URL_with_params = "https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
spelled_out_URL_with_data = "https://api.openweathermap.org/data/2.5/forecast?lat=25.672939&lon=-100.309731&appid=e4c3fc080f6967ebb2401b33c54cf7c1"


# TODO: 1) Make an API Request
# TODO: 2) Get the Forecast in JSON format
# TODO: 3) Twilio Messaging for 12-Hour Heads up Notification


# should rain here soon:
lat = 39.264252   # lat for Parkersburg, Ohio
lon = -81.591698   # lon for Parkersburg, Ohio

#OR current location:
# lat = 25.672939   # lat for MTY, Mexico
# lon = -100.309731   # lon for MTY, Mexico


#------------------ END OF WEATHER VARIABLE SETUP ------------------------ #
#
#------------------ START OF TWILIO (SMS TEXTING) VARIABLE SETUP ------------------------ #

account_sid = os.environ.get('ACCOUNT_SID')    # account_sid for Twilio
print(f"The account_sid is: {account_sid}")     # account_sid for Twilio

auth_token = os.environ.get('AUTH_TOKEN')      # auth_token for Twilio
print(f"The auth_token is: {auth_token}")      # auth_token for Twilio

client = Client(account_sid, auth_token)

#------------------ END OF TWILIO (SMS TEXTING) VARIABLE SETUP ------------------------ #

# Only optional IF you don't place all the data in the updated URL:
weather_params = {
    "lat": lat,
    "lon": lon,
"appid": api_key,
    "cnt": 4,
}

# Place the spelled_out_URL_with_data into a browser:

API_Key_Attempt1 = "https://api.openweathermap.org/data/2.5/weather?lat=25.672939&lon=-100.309731&appid=e4c3fc080f6967ebb2401b33c54cf7c1"
#once waited 2 hours for approval and verification:

# This part is not part of the JSon file:
# // 20240123181946
# // https://api.openweathermap.org/data/2.5/forecast?lat=25.672939&lon=-100.309731&appid=e4c3fc080f6967ebb2401b33c54cf7c1

# JSON_file = ''''''



response = requests.get(url=API_Weather_URL_Endpoint, params=weather_params)

# OR

# response = requests.get(url="https://api.openweathermap.org/data/2.5/weather?lat=25.672939&lon=-100.309731&appid=e4c3fc080f6967ebb2401b33c54cf7c1")
# print(response.raise_for_status())

data = response.json()
print(f"The JSON data is: {data}")

print(f"The status code (response code - for calling this API) is: {data['cod']}")
print(f"The response is: {response.raise_for_status()}")
response.raise_for_status()   #to ACTUALLY raise an Exception to catch any other Response Codes (other than 200)

weather_id_0 = data['list'][0]['weather'][0]['id']
weather_id_1 = data['list'][1]['weather'][0]['id']
weather_id_2 = data['list'][2]['weather'][0]['id']
weather_id_3 = data['list'][3]['weather'][0]['id']
# description = data['list'][0]['weather'][0]['description']

print(f"The weather condition0: {weather_id_0}")
print(f"The weather condition1: {weather_id_1}")
print(f"The weather condition2: {weather_id_2}")
print(f"The weather condition3: {weather_id_3}\n")
# print(f"The weather description: {description}")

# if weather_id_0 < 600 or weather_id_1 < 600 or weather_id_2 < 600 or weather_id_3 < 600:
#     print("Definitely bring an umbrella!")


will_rain = False
for hour_data in data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 600:
        will_rain = True
if will_rain:
    print("Bring an umbrella!") # OR you would enter all the Twilio code below (but still in this IF BLOCK)
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="Greeeeetings! This is a 12-Hour heads up, that it will rain in Monterrey, Mexico!☂️! Wear a poncho!!",
        from_="+18888462616",
        # to='+16198800164',  #toggle this on and the one below this toggled off, to easily swap phone numbers
        to='+17654189611',     #toggle this on and the one above this toggled on, to easily swap phone numbers
        # to='+COUNTRYCODETHENFULLPHONENUMBER',
    )
    print(f"Message Status: {message.status}")


    #IF SMS WORKING, DISABLE BELOW HERE:


    # subject = f"Subject: Your 12 Hour heads up of precipitation!!!\n\n"  # {birthday_person.name}
    # body = "It's going to rain within 12 hours here. Bring an umbrella!"
    # email_being_sent_to2 = "test1.omega1000@gmail.com"
    #
    # with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    #     connection.starttls()
    #     connection.login(user=my_email1, password=my_email_app_password)
    #     connection.sendmail(
    #         from_addr=my_email1,
    #         to_addrs=email_being_sent_to2,
    #         msg=f"{subject}{body}"
    #     )

