import pytest
from bokeh.palettes import Category10, Category20
from bokeh.plotting import show

import app.graph as graph
import app.getdata as getdata

DATA = getdata.import_owid_data()

COUNTRIES = ['Germany', 'Netherlands', 'Slovakia', 'United Kingdom']
COLOURS1 = Category10[max(len(COUNTRIES), 3)]

COLOURS2 = Category20[max(len(COUNTRIES) * 2, 6)]  # Category20 does not work with an input of <3
COLOURS2 = [COLOURS2[2 * i + 1] for i in range(len(COUNTRIES))]


# Test of Country class

def test_init_country():
    for c in COUNTRIES:
        graph.Country(DATA, c)


def test_r_number():
    germany = graph.Country(DATA, 'Germany')
    print(germany.r_number)


def test_active_cases():
    germany = graph.Country(DATA, 'Germany')
    print(germany.active_cases)


def test_cases_by_population():
    germany = graph.Country(DATA, 'Germany')
    print(germany.cases_by_population)


def test_current_cases_by_population():
    germany = graph.Country(DATA, 'Germany')
    print(germany.current_cases_by_population)


def test_deaths_by_population():
    germany = graph.Country(DATA, 'Germany')
    print(germany.deaths_by_population)


def test_vaccinations_by_population():
    germany = graph.Country(DATA, 'Germany')
    print(germany.vaccinations_by_population)


def test_total_vaccinations_by_population():
    germany = graph.Country(DATA, 'Germany')
    print(germany.total_vaccinations_by_population)


def test_total_vaccinated_by_population():
    germany = graph.Country(DATA, 'Germany')
    print(germany.total_vaccinated_by_population)


def test_total_fully_vaccinated_by_population():
    germany = graph.Country(DATA, 'Germany')
    print(germany.total_fully_vaccinated_by_population)


# Test of graphing function
@pytest.mark.parametrize('country', ['Germany', 'Netherlands', 'Slovakia', 'United Kingdom'])
def test_graph_current_cases_country(country):
    g = graph.graph_current_cases(DATA, [country], COLOURS1)
    show(g)


def test_graph_current_cases():
    g = graph.graph_current_cases(DATA, COUNTRIES, COLOURS1)
    show(g)


def test_graph_vaccinated():
    g = graph.graph_vaccinated(DATA, COUNTRIES, COLOURS1, COLOURS2)
    show(g)


def test_graph_cases():
    g = graph.graph_cases(DATA, COUNTRIES, COLOURS1)
    show(g)


def test_graph_r_number():
    g = graph.graph_r_number(DATA, COUNTRIES, COLOURS1)
    show(g)


def test_graph_deaths():
    g = graph.graph_deaths(DATA, COUNTRIES, COLOURS1)
    show(g)


def test_graph_vaccinations():
    g = graph.graph_vaccinations(DATA, COUNTRIES, COLOURS1)
    show(g)


def test_make_graphs():
    graph.make_graphs(DATA, COUNTRIES)
