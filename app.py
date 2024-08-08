from flask import Flask,render_template,request, jsonify,redirect,url_for
import requests



app = Flask(__name__)




@app.route('/', methods=["GET", "POST"])
def index():   
    if request.method == 'POST':
     input = request.form.get("city") or "london"
     return redirect(url_for("current", **{"result": input}))
    else:
        cities = [
                    "New York",
                    "Los Angeles",
                    "Chicago",
                    "Toronto",
                    "Tokyo",
                    "Paris",
                    "Berlin",
                    "Sydney",
                    "Moscow",
                    "Dubai",
                    "Hong Kong",
                    "London",   
                    "Manchester" 
                    "Birmingham" 
                    ]
        weather_data = {}
        for city in cities:
            url = f"https://api.weatherapi.com/v1/current.json?key=607a20de772b46a8ad823818230512&q={city}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                current_weather = data.get('current', {})
                location = data.get('location', {})
                
                # Extract relevant details
                city_name = location.get('name', 'Unknown')
                temp_c = current_weather.get('temp_c', 0)
                condition_text = current_weather.get('condition', {}).get('text', 'No condition')
                icon_url = current_weather.get('condition', {}).get('icon', '')
                humidity = current_weather.get('humidity', 0)
                wind_mph = current_weather.get('wind_mph', 0)
                
                weather_data[city_name] = {
                    'Temp': round(temp_c),
                    'condition': condition_text,
                    'icon': f"https:{icon_url}",
                    'humidity': humidity,
                    'windspeed': round(wind_mph)
                }
        
        return render_template("index.html", weather_data=weather_data)
 
   


@app.route('/current')
def current():
    # Get the city name from the query parameter
    result = request.args.get('result') or "Paris"
    
    # List of cities to display below the current city
    other_cities = ["New York", "Los Angeles", "Chicago", "Toronto", "Tokyo", "Paris", "Berlin", "Sydney", "Moscow", "Dubai", "Hong Kong", "London", "Manchester", "Birmingham"]
    
    # Fetch weather data for the current city
    current_city_url = f"https://api.weatherapi.com/v1/current.json?key=607a20de772b46a8ad823818230512&q={result}"
    current_response = requests.get(current_city_url)
    
    # Initialize dictionaries to hold weather data
    current_weather_data = {}
    other_weather_data = {}
    
    # Determine the background image for the current city
    city_backgrounds = {
        "New York": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Los Angeles": "https://images.unsplash.com/photo-1518416177092-ec985e4d6c14?q=80&w=2832&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Chicago": "https://images.unsplash.com/photo-1494522358652-f30e61a60313?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Toronto": "https://images.unsplash.com/photo-1557887727-84ea242c5042?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8dG9ycm9udG98ZW58MHwwfDB8fHwy",
        "Tokyo": "https://images.unsplash.com/photo-1480796927426-f609979314bd?q=80&w=2300&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2946&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Berlin": "https://images.unsplash.com/photo-1546726747-421c6d69c929?q=80&w=2832&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Sydney": "https://images.unsplash.com/photo-1528072164453-f4e8ef0d475a?q=80&w=2942&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Moscow": "https://plus.unsplash.com/premium_photo-1697730206914-f013a9fa5174?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Hong Kong": "https://images.unsplash.com/photo-1554208786-6776fa9e7df4?q=80&w=2946&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "Istanbul": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?q=80&w=2549&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "default": "https://images.unsplash.com/photo-1561485039-765c8e81686d?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",}
    
    current_background =  city_backgrounds.get(result,  city_backgrounds["default"])
    
    if current_response.status_code == 200:
        current_data = current_response.json()
        current_weather = current_data.get('current', {})
        location = current_data.get('location', {})
        
        # Extract current city weather details
        current_weather_data = {
            'cityName': location.get('name', 'Unknown'),
            'Temp': round(current_weather.get('temp_c', 0)),
            'condition': current_weather.get('condition', {}).get('text', 'No condition'),
            'icon': f"https:{current_weather.get('condition', {}).get('icon', '')}",
            'humidity': current_weather.get('humidity', 0),
            'windspeed': round(current_weather.get('wind_mph', 0))
        }
    
    # Fetch weather data for other cities
    for city in other_cities:
        other_city_url = f"https://api.weatherapi.com/v1/current.json?key=607a20de772b46a8ad823818230512&q={city}"
        other_response = requests.get(other_city_url)
        if other_response.status_code == 200:
            other_data = other_response.json()
            other_current_weather = other_data.get('current', {})
            other_location = other_data.get('location', {})
            
            # Extract weather details for other cities
            city_name = other_location.get('name', 'Unknown')
            temp_c = other_current_weather.get('temp_c', 0)
            condition_text = other_current_weather.get('condition', {}).get('text', 'No condition')
            icon_url = other_current_weather.get('condition', {}).get('icon', '')
            humidity = other_current_weather.get('humidity', 0)
            wind_mph = other_current_weather.get('wind_mph', 0)
            
            other_weather_data[city_name] = {
                'Temp': round(temp_c),
                'condition': condition_text,
                'icon': f"https:{icon_url}",
                'humidity': humidity,
                'windspeed': round(wind_mph)
            }
    
    # Render the template with both current city data and other cities' data
    return render_template(
        "current.html",
        current_weather=current_weather_data,
        other_weather_data=other_weather_data,
        background_image=current_background
    )

    # Get the city name from the query parameter
    result = request.args.get('result') or "Paris"
    
    # List of cities to display below the current city
    other_cities = ["Paris", "Rome", "Oslo", "Dublin"]
    
    # Fetch weather data for the current city
    current_city_url = f"https://api.weatherapi.com/v1/current.json?key=607a20de772b46a8ad823818230512&q={result}"
    current_response = requests.get(current_city_url)
    
    # Initialize dictionaries to hold weather data
    current_weather_data = {}
    other_weather_data = {}
    
    if current_response.status_code == 200:
        current_data = current_response.json()
        current_weather = current_data.get('current', {})
        location = current_data.get('location', {})
        
        # Extract current city weather details
        current_weather_data = {
            'cityName': location.get('name', 'Unknown'),
            'Temp': round(current_weather.get('temp_c', 0)),
            'condition': current_weather.get('condition', {}).get('text', 'No condition'),
            'icon': f"https:{current_weather.get('condition', {}).get('icon', '')}",
            'humidity': current_weather.get('humidity', 0),
            'windspeed': round(current_weather.get('wind_mph', 0))
        }
    
    # Fetch weather data for other cities
    for city in other_cities:
        other_city_url = f"https://api.weatherapi.com/v1/current.json?key=607a20de772b46a8ad823818230512&q={city}"
        other_response = requests.get(other_city_url)
        if other_response.status_code == 200:
            other_data = other_response.json()
            other_current_weather = other_data.get('current', {})
            other_location = other_data.get('location', {})
            
            # Extract weather details for other cities
            city_name = other_location.get('name', 'Unknown')
            temp_c = other_current_weather.get('temp_c', 0)
            condition_text = other_current_weather.get('condition', {}).get('text', 'No condition')
            icon_url = other_current_weather.get('condition', {}).get('icon', '')
            humidity = other_current_weather.get('humidity', 0)
            wind_mph = other_current_weather.get('wind_mph', 0)
            
            other_weather_data[city_name] = {
                'Temp': round(temp_c),
                'condition': condition_text,
                'icon': f"https:{icon_url}",
                'humidity': humidity,
                'windspeed': round(wind_mph)
            }
    
    # Render the template with both current city data and other cities' data
    return render_template(
        "current.html",
        current_weather=current_weather_data,
        other_weather_data=other_weather_data
    )

    result = request.args.get('result') or "paris"
    url = f"https://api.weatherapi.com/v1/current.json?key=607a20de772b46a8ad823818230512&q={result}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Convert the response to JSON
   # Extract current weather and location data
        current_weather = data.get('current', {})
        location = data.get('location', {})
        
        # Extract relevant details
        city_name = location.get('name', 'Unknown')
        temp_c = current_weather.get('temp_c', 0)
        condition_text = current_weather.get('condition', {}).get('text', 'No condition')
        icon_url = current_weather.get('condition', {}).get('icon', '')
        humidity = current_weather.get('humidity', 0)
        wind_mph = current_weather.get('wind_mph', 0)
        
        
        
        
        # Return both current weather and location in the response
        return render_template("current.html",
            current_weather=current_weather,
            location=location,
            cityName=location["name"],
            Temp=round(current_weather["temp_c"]),
            condition=current_weather["condition"]["text"],
            icon=f"https:{icon_url}",
            humidity=current_weather["humidity"],
            windspeed=round(current_weather["wind_mph"]),
            
        )
    else:
        # Return an error message if the request failed
        return jsonify({"error": f"Error fetching weather data: {response.status_code}"}), response.status_code

 

    return full.json()

if __name__ == "__main__":
    app.run(debug=True,port=5000)