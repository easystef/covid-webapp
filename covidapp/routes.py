from flask import Flask, request
from covidapp import getdata
from covidapp.graph import Country

app = Flask(__name__)


@app.route("/")
def covid():

    countries = ['Germany', 'Netherlands', 'Slovakia', 'United Kingdom']
    data = getdata.import_owid_data()

    cases = '<ul>'
    vaccinations = '<ul>'

    for country in countries:
        my_country = Country(data, country)

        cases = cases + '<li>' + f'{country}: ' + str(round(my_country.current_cases_by_population)) + '</li>'

        vaccinations = vaccinations + '<li>' + f'{country}: ' \
                       + str(round(my_country.total_vaccinations_by_population)) + '</li>'

    cases = cases + '</ul>'
    vaccinations = vaccinations + '</ul>'

    return (
        """<h1>Covid Dashboard</h1>
        <h3>Current cases in previous week per 100k people</h3>"""
        + cases
        + """<h3>Total vaccinations so far per 100 people</h3>"""
        + vaccinations
    )


def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    try:
        fahrenheit = float(celsius) * 9 / 5 + 32
        fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
        return str(fahrenheit)
    except ValueError:
        return "invalid input"

