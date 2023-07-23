from flask import Flask, render_template, request
from weather import get_weather

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # ensure to have the value of data when we load the page to avoid errors
    data = None

    if request.method == 'POST':
        city = request.form['city_name']
        state = request.form['state_name']
        country = request.form['country_name']
        data = get_weather(city, state, country)

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)