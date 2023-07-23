import requests
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# load environment variables
load_dotenv
# get open weather api key from loaded environment variables.
open_weather_api_key = os.getenv('API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# setup database if it doesn't exist
with app.app_context():
    db.create_all()

def get_weather_data(city):
    request_url = f'{BASE_URL}?q={city}&units=metric&appid={open_weather_api_key}'
    data = requests.get(request_url).json()
    return data


@app.route('/', methods=['GET'])
def weather_data():
    # if method is GET
    cities = City.query.all()

    weather_data = []

    for city in cities:

        data = get_weather_data(city.name)

        weather = {
            'city': city.name,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

@app.route('/', methods=['POST'])
def add_city():
    err_msg = ''
    city = request.form.get('city')

    # check if city has value
    if city:
        city_exists = City.query.filter_by(name=city).first()
        
        # check to see if the city is already in db
        if not city_exists:
            city_weather_data = get_weather_data(city)
            if city_weather_data['cod'] == 200:
                new_city = City(name=city)
                db.session.add(new_city)
                db.session.commit()
                # flash message here
            else:
                err_msg = 'City does not exist!'
        else:
            err_msg = 'City already exists in the database!'
    
    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added successfully!')

    return redirect(url_for('weather_data'))

@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted {city.name}', 'success')
    return redirect(url_for('weather_data'))

if __name__ == '__main__':
    app.run(debug=True)
