from bokeh.embed import components
from flask import Flask, render_template, request
from bokeh.plotting import figure, show
from app import getdata
from app import graph
from app.graph import Country


app = Flask(__name__)

# @app.route("/")
# def covid():
#     countries = ['Germany', 'Netherlands', 'Slovakia', 'United Kingdom']
#     data = getdata.import_owid_data()
#
#     cases = '<ul>'
#     vaccinations = '<ul>'
#
#     for country in countries:
#         my_country = Country(data, country)
#
#         cases = cases + '<li>' + f'{country}: ' + str(round(my_country.current_cases_by_population)) + '</li>'
#
#         vaccinations = vaccinations + '<li>' + f'{country}: ' \
#                        + str(round(my_country.total_vaccinations_by_population)) + '</li>'
#
#     cases = cases + '</ul>'
#     vaccinations = vaccinations + '</ul>'
#
#     return (
#         """<h1>Covid Dashboard</h1>
#         <h3>Current cases in previous week per 100k people</h3>"""
#         + cases
#         + """<h3>Total vaccinations so far per 100 people</h3>"""
#         + vaccinations
#     )


@app.route("/")
def covid():

    # Prepare data
    countries = ['Germany', 'Netherlands', 'Slovakia', 'United Kingdom']
    data = getdata.import_owid_data()

    plot = graph.plot_current_cases(data, countries)
    #plot = figure()  # TODO delete
    #plot.circle([1, 2], [3, 4])    # TODO delete
    #show(plot)    # TODO delete
    script, div = components(plot)

    return render_template('dashboard.html', the_div=div, the_script=script)




