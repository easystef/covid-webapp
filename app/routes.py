""" routes.py

Application routes for the different pages of the web application.
 - "/" Coronavirus Dashboard

"""

from bokeh.embed import components
from flask import render_template

from app import app
from app import getdata
from app import graph


@app.route("/")
def covid():
    """ Generates the relevant graphs based on OWID data and displays it in the template dashboard.html. Graphs
    generated for:
        - Germany
        - Netherlands
        - Slovakia
        - United Kingdom
        - European Union

    :return: dashboard.html page with current data
    """

    # Prepare data
    countries = ('Germany', 'Netherlands', 'Slovakia', 'United Kingdom', 'European Union')
    data = getdata.import_owid_data()

    current_cases, total_vaccinations, cases, r_number, deaths, vaccinations = graph.make_graphs(data, countries)

    plots1 = {'current_cases': current_cases, 'total_vaccinations': total_vaccinations}
    script1, div1 = components(plots1)

    plots2 = {'cases': cases, 'r_number': r_number, 'deaths': deaths, 'vaccinations': vaccinations}
    script2, div2 = components(plots2)

    return render_template('dashboard.html', the_div1=div1, the_script1=script1, the_div2=div2, the_script2=script2)


@app.route("/country/<string:country>")
def covid_by_country(country):
    """ Generates the relevant graphs based on OWID data and displays it in the template dashboard.html. Graphs
    generated for single specified country.

    :param country: country for which the charts should be constructed as a string
    :return: dashboard.html page with current data
    """

    # Prepare data
    country = [country]
    print(country)
    print(type(country))
    data = getdata.import_owid_data()

    current_cases, vaccinated, cases, r_number, deaths, vaccinations = graph.make_graphs(data, country)

    plots1 = {'current_cases': current_cases, 'vaccinated': vaccinated}
    script1, div1 = components(plots1)

    plots2 = {'cases': cases, 'r_number': r_number, 'deaths': deaths, 'vaccinations': vaccinations}
    script2, div2 = components(plots2)

    return render_template('dashboard.html', the_div1=div1, the_script1=script1, the_div2=div2, the_script2=script2)
