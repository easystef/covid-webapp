import pandas as pd

OWID_DATA_URL = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'


def import_owid_data():
    """Reads coronavirus data for Our World In Data

    Loads the data and formats the dates

    :return: pandas.DataFrame
        Containing the data from Our World In Data
    """

    owid_data = pd.read_csv(OWID_DATA_URL, encoding='utf_8')
    owid_data['date'] = pd.to_datetime(owid_data['date'], format='%Y-%m-%d')

    return owid_data

# Start static
# TODO for each country get the last value of population into a dataframe
# TODO write the data into covid_data.db
# TODO create table for other data
# TODO fill table with most recent data
# TODO fill models.py
# TODO write simple app that for a given set of countries reads the data and returns the cases per 100k, avg vaccine per 100, and r-number and prints them as a tree via cli

# Introduce data updates
# TODO check for and identify new data
# TODO write new data to database if available

'''
Later...
- Add a web front end using flask
- Reintroduce graphs
- Packaging Flask?
'''
