from bokeh.embed import components
from bokeh.palettes import Category10
from flask import Flask, render_template
from app import getdata
from app import graph


app = Flask(__name__)


@app.route("/")
def covid():

    # Prepare data
    countries = ['Germany', 'Netherlands', 'Slovakia', 'United Kingdom']
    data = getdata.import_owid_data()
    
    # Set colour scheme
    colours = Category10[max(len(countries), 3)]  # Category10 does not work with an input of <3
    if len(countries) > len(colours):
        raise ValueError(f"The maximum number of countries which can be plotted is {len(colours)}")

    p1 = graph.graph_current_cases(data, countries, colours)
    p2 = graph.graph_total_vaccinations(data, countries, colours)

    p3 = graph.graph_cases(data, countries, colours)
    p4 = graph.graph_r_number(data, countries, colours)
    p5 = graph.graph_deaths(data, countries, colours)
    p6 = graph.graph_vaccinations(data, countries, colours)

    plots1 = {'current_cases': p1, 'total_vaccinations': p2}
    script1, div1 = components(plots1)

    plots2 = {'cases': p3, 'r_number': p4, 'deaths': p5, 'vaccinations': p6}
    script2, div2 = components(plots2)

    return render_template('dashboard.html', the_div1=div1, the_script1=script1, the_div2=div2, the_script2=script2)