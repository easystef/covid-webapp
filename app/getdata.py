import pandas as pd

OWID_DATA_URL = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'


# TODO class and function documenation
def import_owid_data():
    """Reads coronavirus data for Our World In Data

    Loads the data and formats the dates

    :return: pandas.DataFrame
        Containing the data from Our World In Data
    """

    owid_data = pd.read_csv(OWID_DATA_URL, encoding='utf_8')
    owid_data['date'] = pd.to_datetime(owid_data['date'], format='%Y-%m-%d')

    return owid_data
