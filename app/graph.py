# TODO module documentation

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.annotations import Span
from bokeh.plotting import figure

OWID_DATA_URL = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'


class Country:
    # TODO class documentation

    def __init__(self, covid_data, country_name):
        # Prepare data
        country_data = covid_data[covid_data['location'] == country_name]
        country_data.set_index('date', drop=False, inplace=True)

        self.date = country_data['date'].sort_index()
        self.cases = country_data['new_cases'].sort_index()
        self.deaths = country_data['new_deaths'].sort_index()
        total_vaccinations = country_data['total_vaccinations'].interpolate(method='linear').sort_index()
        self.vaccinations = total_vaccinations.diff()
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


# TODO add function docuemntation to everything below
# TODO fix drop off in vaccines when there is not data
# BOKEH GRAPH FUNCTIONS --------------------------

def graph_current_cases(data, countries, colours):

    hover = HoverTool(tooltips=[('cases', '@current_cases{0.0}')])
    p = figure(y_range=countries, width=600, height=300, title="Current cases in previous week per 100k people",
               toolbar_location=None, tools=[hover])

    current_cases = []

    for i, country in enumerate(countries):
        my_country = Country(data, country)
        current_cases.append(my_country.current_cases_by_population)

    source = ColumnDataSource(data=dict(countries=countries, current_cases=current_cases, color=colours))
    p.hbar(y='countries', right='current_cases', left=0, height=0.6, color='color', source=source)

    return p


def graph_total_vaccinations(data, countries, colours):
    
    hover = HoverTool(tooltips=[('vaccinations', '@total_vaccination{0.0}')])
    p = figure(y_range=countries, width=600, height=300, title="Total vaccinations per 100 people",
               toolbar_location=None, tools=[hover])
                
    total_vaccination = []
    
    for i, country in enumerate(countries):
        my_country = Country(data, country)
        total_vaccination.append(my_country.total_vaccinations_by_population)
        
    source = ColumnDataSource(data=dict(countries=countries, total_vaccination=total_vaccination, color=colours))
    p.hbar(y='countries', right='total_vaccination', left=0, height=0.6, color='color', source=source)
    
    return p


def graph_cases(data, countries, colours):
    
    hover = HoverTool(tooltips=[('country', '$name'), ('date', '$x{%F}'), ('cases', '$y{0,0}')],
                      formatters={'$x': 'datetime'})
    p = figure(width=600, height=300, title="Cases in previous week per 100k people", tools=[hover],
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
    
    hover = HoverTool(tooltips=[('country', '$name'), ('date', '$x{%F}'), ('r-number', '$y')],
                      formatters={'$x': 'datetime'})
    p = figure(width=600, height=300, title="R-Number", tools=[hover], x_axis_type="datetime", x_axis_label='date',
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

    hover = HoverTool(tooltips=[('country', '$name'), ('date', '$x{%F}'), ('deaths', '$y{0.0}')],
                      formatters={'$x': 'datetime'})
    p = figure(width=600, height=300, title="Deaths in previous week per 100k people", tools=[hover],
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

    hover = HoverTool(tooltips=[('country', '$name'), ('date', '$x{%F}'), ('vaccinations', '$y{0.00}')],
                      formatters={'$x': 'datetime'})
    p = figure(width=600, height=300, title="Average vaccinations in last 7 days per 100 people", tools=[hover],
               x_axis_type="datetime", x_axis_label='date', y_axis_label='vaccinations', toolbar_location=None)
    p.xaxis.formatter.days = '%d-%b'
    p.y_range.start = 0

    for i, country in enumerate(countries):
        my_country = Country(data, country)
        s = my_country.vaccinations_by_population[-60:]
        p.line(s.index, s.values, name=country, legend_label=country, line_width=2, line_color=colours[i])

    p.legend.location = 'top_left'

    return p


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
