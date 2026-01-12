import requests
import os
from flask import Flask,jsonify,request,render_template
from dotenv import load_dotenv
load_dotenv()

#@app.route("/weather")
app=Flask(__name__)
OPEN_WEATHER_API_KEY=os.getenv("OPEN_WEATHER_API_KEY")
if(not OPEN_WEATHER_API_KEY):
    raise RuntimeError("key not found")
def weather(API_key,city_name,country_code,limit):
    
    url2=f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit={limit}&appid={API_key}"
    try:
        headers={
            "User-agent":"BAB109",
            "Accept":"application/json"
        }
        #if(API_key):
        #    headers["aurtorization"]=API_key
        response=requests.get(url2,headers=headers,timeout=10)
        response.raise_for_status()
        result=response.json()
        
        print(f"status code for coords:{response.status_code}")
        if not result :
            return None
        data=result[0]
        lat=data.get("lat")
        lon=data.get("lon")
        print(f"{lat}\n{lon}")
        
        url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"
        response_2=requests.get(url,headers=headers,timeout=10)
        response_2.raise_for_status()
        print(f"status code for weather:{response_2.status_code}")
        #return response_2.json()
        data = response_2.json()

        temp_kelvin = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        temp_celsius = round(temp_kelvin - 273.15, 2)

        return {
            "city": city_name,
            "temperature": temp_celsius,
            "humidity": humidity
        }
    except requests.exceptions.HTTPError as err:
        print(f"http error:{err}")
    except requests.exceptions.ConnectionError as er:
        print(f"CONNeCTON ERR:{er}")
    except requests.Timeout as err:
        print(f"Time ouT error:{err}")
    except Exception as e:
        print(f"unknown error cought:{e}")
#data=weather(OPEN_WEATHER_API_KEY,"New Delhi","IN",3)
@app.route("/")
def home():
    return render_template("UI.html")

@app.route("/weather")
def info():
    city = request.args.get("city")
    country = request.args.get("country")

    if not city or not country:
        return jsonify({"error": "Missing city or country"}), 400

    result = weather(OPEN_WEATHER_API_KEY, city, country, 1)
    return jsonify(result)
if __name__ == "__main__":
    app.run(debug=True)