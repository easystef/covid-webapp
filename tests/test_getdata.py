import pandas as pd

import app.getdata as getdata


def test_import_owid_data():

    data = getdata.import_owid_data()

    assert(isinstance(data, pd.DataFrame))
    for c in ['date', 'new_cases', 'new_deaths', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
              'population']:
        assert c in data.columns
