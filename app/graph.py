""" graph.py

1. Class for preparing data based on inputs
2. Functions for generating each of the graphs to be displayed
"""

from bokeh.models import HoverTool, ColumnDataSource, Range1d
from bokeh.models.annotations import Span
from bokeh.palettes import Category10, Category20
from bokeh.plotting import figure
from numpy import isnan

CHART_WIDTH = 600
CHART_HEIGHT = 300
CHART_SIZING = 'scale_both'


class Country:
    """ A simple class which takes the coronavirus data and for a specified country generates statistics and series
    for graphing.
    """

    def __init__(self, covid_data, country_name):
        """Initialises the Country object for the specified country. Generates:
            - date: series of dates (pandas.Series)
            - cases: number of coronavirus cases each day (pandas.Series)
            - deaths: number of coronavirus related deaths each day (pandas.Series)
            - vaccinations: number of coronavirus vaccinations each day (pandas.Series)
            - population: population of the country (float)

        :param covid_data: pandas.DataFrame containing the following daily series
            - 'date': dates
            - 'new_cases': number of coronavirus cases each day
            - 'new_deaths': number of coronavirus related deaths each day
            - 'total_vaccinations': total vaccinations up to and included that day
            - 'population': population of the country
        :param country_name:
        """

        # Prepare data
        country_data = covid_data[covid_data['location'].str.lower() == country_name.lower()]
        country_data.set_index('date', drop=False, inplace=True)

        self.date = country_data['date'].sort_index()
        self.cases = country_data['new_cases'].sort_index()
        self.deaths = country_data['new_deaths'].sort_index()
        total_vaccinations = country_data['total_vaccinations'].interpolate(method='linear').sort_index()
        self.vaccinations = self.trunc_data(total_vaccinations.diff())
        self.vaccinated = self.trunc_data(country_data['people_vaccinated'].sort_index())
        self.fully_vaccinated = self.trunc_data(country_data['people_fully_vaccinated'].sort_index())
        self.population = country_data['population'][0]

    def r_number(self, lag=1, n_days=1):
        """Calculates a simple version of the R-number - the number of additional people infected by each infected
        individual.

        It is calculated as the ratio of the total number of infected people over a specified period, divided by the
        number of people infected over a period of the same length of time in an earlier period.

        :param lag: integer, default 1
            The number of days between the two periods in which the infection rate is being measured.
        :param n_days: integer, default 1
            The length of the period over which the number of infections is being counted for the two periods.
        :return: pandas.Series
            Containing the resulting R-number
        """

        x = self.cases.rolling(n_days).sum()
        x_lag = x.shift(lag)

        return x / x_lag

    @property
    def active_cases(self, recovery_days=14):
        """Calculates the number of active cases at any given point in time.

        For simplicity, it is assumed that people all recover after the same fixed number of days. Two weeks, by
        default.

        :param recovery_days: integer, default 14
            The number of days a newly infected person is assumed to be sick.
        :return: pandas.Series
            Containing the resulting number of active cases each day
        """

        return self.cases.rolling(recovery_days).sum()

    @property
    def cases_by_population(self):
        """The number of cases over the last 7 days per 100k people.

        :return: pandas.Series
            Resulting number of cases
        """

        return self.cases.rolling(7).sum() / (self.population / 100000)

    @property
    def current_cases_by_population(self):
        """The current number of cases over the last 7 days per 100k people.

        :return: integer
            Resulting number of cases
        """

        return self.cases_by_population[-1]

    @property
    def deaths_by_population(self):
        """The number of cases over the last 7 days per 100k people.

        :return: pandas.Series
            Resulting number of deaths
        """

        return self.deaths.rolling(7).sum() / (self.population / 100000)

    @property
    def vaccinations_by_population(self):
        """The average number of vaccinations over the last 7 days per 100 people.

        :return: pandas.Series
            Resulting number of vaccinations
        """

        return self.vaccinations.rolling(7).mean() / (self.population / 100)

    @property
    def total_vaccinations_by_population(self):
        """The most recent total number of vaccinations per 100 people

        :return: integer
            Total number
        """

        return self.vaccinations.sum() / (self.population / 100)

    @property
    def total_vaccinated_by_population(self):
        """The total number of people who have had at least one dose of the vaccine as a percentage of the population.

        :return: integer
            Total number
        """

        return self.vaccinated[-1] / self.population * 100

    @property
    def total_fully_vaccinated_by_population(self):
        """The total number of people who are fully vaccinated as a percentage of the population.

        :return: integer
            Total number
        """

        return self.fully_vaccinated[-1] / self.population * 100

    @staticmethod
    def trunc_data(x):
        """Truncates zeros at the end of a Series

        Looks at the last 7 values of a series and truncates the series to omit the zeros. The function is intended
        for fixing series where there are missing values at the end and these are entered as zeros rather than NaNs.

        :param x: pandas.Series
            Series to be truncated
        :return: pandas.Series
            Truncated series
        """

        for i in range(7):
            if x[-1] == 0 or isnan(x[-1]):
                x = x[:-1]

        return x


# BOKEH GRAPH FUNCTIONS --------------------------

def graph_current_cases(data, countries, colours):
    """ Generates Bokeh horizontal bar charts showing current cases in the previous week per 100k people.

    :param data: pandas.Dataframe containing data for the relevant countries
    :param countries: countries to be graphed given as a list of strings
    :param colours: colour scheme from bokeh.palettes
    :return: horizontal bar chart
    """

    hover = HoverTool(tooltips=[('cases', '@current_cases{0.0}')])
    p = figure(y_range=countries, width=CHART_WIDTH, height=CHART_HEIGHT, sizing_mode=CHART_SIZING, title="Current cases in previous week per 100k people",
               toolbar_location=None, tools=[hover])

    current_cases = []

    for i, country in enumerate(countries):
        my_country = Country(data, country)
        current_cases.append(my_country.current_cases_by_population)

    source = ColumnDataSource(data=dict(countries=countries, current_cases=current_cases, color=colours))
    p.hbar(y='countries', right='current_cases', left=0, height=0.6, color='color', source=source)

    return p


def graph_vaccinated(data, countries, colours1, colours2):
    """ Generates Bokeh stacked horizontal bar charts showing the percentage of the population that has been vaccinated
     and the percentage of the population fully vaccinated.

    :param data: pandas.Dataframe containing data for the relevant countries
    :param countries: countries to be graphed given as a list of strings
    :param colours1: colour scheme from bokeh.palettes (used for fully vaccinated)
    :param colours2: second colour scheme from bokeh.palettes (used for vaccinated)
    :return: horizontal bar chart
    """
    
    hover = HoverTool(tooltips=[('fully vaccinated', '@fully_vaccinated{0.0}'), ('vaccinated', '@vaccinated{0.0}')])
    p = figure(y_range=countries, width=CHART_WIDTH, height=CHART_HEIGHT, sizing_mode=CHART_SIZING, title="Percentage of the population that has been vaccinated",
               toolbar_location=None, tools=[hover])
    p.x_range = Range1d(0, 100)
                
    vaccinated = []
    fully_vaccinated = []
    
    for i, country in enumerate(countries):
        my_country = Country(data, country)
        vaccinated.append(my_country.total_vaccinated_by_population)
        fully_vaccinated.append(my_country.total_fully_vaccinated_by_population)
        
    source = ColumnDataSource(data=dict(countries=countries, vaccinated=vaccinated, fully_vaccinated=fully_vaccinated,
                                        color1=colours1, color2=colours2))
    p.hbar(y='countries', right='vaccinated', left=0, height=0.6, color='color2', source=source)
    p.hbar(y='countries', right='fully_vaccinated', left=0, height=0.6, color='color1', source=source)
    
    return p


def graph_cases(data, countries, colours):
    """ Generates Bokeh line charts showing cases in previous week per 100k people

    :param data: pandas.Dataframe containing data for the relevant countries
    :param countries: countries to be graphed given as a list of strings
    :param colours: colour scheme from bokeh.palettes
    :return: line chart
    """
    
    hover = HoverTool(tooltips=[('country', '$name'), ('date', '$x{%F}'), ('cases', '$y{0,0}')],
                      formatters={'$x': 'datetime'})
    p = figure(width=CHART_WIDTH, height=CHART_HEIGHT, sizing_mode=CHART_SIZING, title="Cases in previous week per 100k people", tools=[hover],
               x_axis_type="datetime", x_axis_label='date', y_axis_label='cases', toolbar_location=None)
    p.xaxis.formatter.days = '%d-%b'
    p.y_range.start = 0
    
    for i, country in enumerate(countries):
        my_country = Country(data, country)
        s = my_country.cases_by_population[-60:]
        p.line(s.index, s.values, name=country, legend_label=country, line_width=2, line_color=colours[i])

    p.legend.location = 'top_left'
        
    return p


def graph_r_number(data, countries, colours):
    """ Generates Bokeh line charts showing R-Number

    :param data: pandas.Dataframe containing data for the relevant countries
    :param countries: countries to be graphed given as a list of strings
    :param colours: colour scheme from bokeh.palettes
    :return: line chart
    """
    
    hover = HoverTool(tooltips=[('country', '$name'), ('date', '$x{%F}'), ('r-number', '$y')],
                      formatters={'$x': 'datetime'})
    p = figure(width=CHART_WIDTH, height=CHART_HEIGHT, sizing_mode=CHART_SIZING, title="R-Number", tools=[hover], x_axis_type="datetime", x_axis_label='date',
               y_axis_label='r-number', toolbar_location=None)
    p.xaxis.formatter.days = '%d-%b'

    for i, country in enumerate(countries):
        my_country = Country(data, country)
        s = my_country.r_number(4, 7)[-60:]
        p.line(s.index, s.values, name=country, legend_label=country, line_width=2, line_color=colours[i])
    
    r_one = Span(location=1, dimension='width', line_color='maroon', line_width=2)
    p.add_layout(r_one)
    p.legend.location = 'top_left'
    
    return p


def graph_deaths(data, countries, colours):
    """ Generates Bokeh line charts showing deaths in previous week per 100k people

    :param data: pandas.Dataframe containing data for the relevant countries
    :param countries: countries to be graphed given as a list of strings
    :param colours: colour scheme from bokeh.palettes
    :return: line chart
    """

    hover = HoverTool(tooltips=[('country', '$name'), ('date', '$x{%F}'), ('deaths', '$y{0.0}')],
                      formatters={'$x': 'datetime'})
    p = figure(width=CHART_WIDTH, height=CHART_HEIGHT, sizing_mode=CHART_SIZING, title="Deaths in previous week per 100k people", tools=[hover],
               x_axis_type="datetime", x_axis_label='date', y_axis_label='deaths', toolbar_location=None)
    p.xaxis.formatter.days = '%d-%b'
    p.y_range.start = 0
    
    for i, country in enumerate(countries):
        my_country = Country(data, country)
        s = my_country.deaths_by_population[-60:]
        p.line(s.index, s.values, name=country, legend_label=country, line_width=2, line_color=colours[i])

    p.legend.location = 'top_left'

    return p


def graph_vaccinations(data, countries, colours):
    """ Generates Bokeh line charts showing average vaccinations in last 7 days per 100 people

    :param data: pandas.Dataframe containing data for the relevant countries
    :param countries: countries to be graphed given as a list of strings
    :param colours: colour scheme from bokeh.palettes
    :return: line chart
    """

    hover = HoverTool(tooltips=[('country', '$name'), ('date', '$x{%F}'), ('vaccinations', '$y{0.00}')],
                      formatters={'$x': 'datetime'})
    p = figure(width=CHART_WIDTH, height=CHART_HEIGHT, sizing_mode=CHART_SIZING, title="Average vaccinations in last 7 days per 100 people", tools=[hover],
               x_axis_type="datetime", x_axis_label='date', y_axis_label='vaccinations', toolbar_location=None)
    p.xaxis.formatter.days = '%d-%b'
    p.y_range.start = 0

    for i, country in enumerate(countries):
        my_country = Country(data, country)
        s = my_country.vaccinations_by_population[-60:]
        p.line(s.index, s.values, name=country, legend_label=country, line_width=2, line_color=colours[i])

    p.legend.location = 'top_left'

    return p


def make_graphs(data, countries):
    """Generates six graphs using the input coronavirus data as listed below.

    :param data: pandas.Dataframe containing data for the relevant countries
    :param countries: countries to be graphed given as a list of strings
    :return: six bokeh charts
        - current_cases: Current cases in previous week per 100k people
        - vaccinated: Percentage of the population vaccinated
        - cases: Cases in previous week per 100k people
        - r_number: R-Number
        - deaths: Deaths in previous week per 100k people
        - vaccinations: Average vaccinations in last 7 days per 100 people
    """

    colours = Category10[max(len(countries), 3)]  # Category10 does not work with an input of <3
    if len(countries) > len(colours):
        raise ValueError(f"The maximum number of countries which can be plotted is {len(colours)}")
        
    colours2 = Category20[max(len(countries) * 2, 6)]  # Category20 does not work with an input of <3
    colours2 = [colours2[2 * i + 1] for i in range(len(countries))]

    current_cases = graph_current_cases(data, countries, colours)
    vaccinated = graph_vaccinated(data, countries, colours, colours2)

    cases = graph_cases(data, countries, colours)
    r_number = graph_r_number(data, countries, colours)
    deaths = graph_deaths(data, countries, colours)
    vaccinations = graph_vaccinations(data, countries, colours)

    return current_cases, vaccinated, cases, r_number, deaths, vaccinations


# Legacy code for country specific graphs
"""
def make_graphs(data, countries, colours):

    # Create lists to contain country specific graphs for number of cases per day and number of deaths per day
    cases = []
    deaths = []

    # 2. Create glyphs

    for i, country in enumerate(countries):
        my_country = Country(data, country)

        # Graph 6 - Cases
        p6 = figure(width=600, height=200, title=f'{country} - Cases per Day', x_axis_type="datetime",
                    x_axis_label='date', y_axis_label='cases', toolbar_location=None)
        p6.vbar(my_country.date, top=my_country.cases, color=colours[i])
        p6.xaxis.formatter.months = '%b-%y'

        # Graph 7 - Deaths
        p7 = figure(width=600, height=200, title=f'{country} - Deaths per Day', x_axis_type="datetime",
                    x_axis_label='date', y_axis_label='deaths', toolbar_location=None)
        p7.vbar(my_country.date, top=my_country.deaths, color=colours[i])
        p7.xaxis.formatter.months = '%b-%y'

        cases.append(p6)
        deaths.append(p7)

    # 3. Return the results
    return layout([
        [cases, deaths]
    ])
"""
