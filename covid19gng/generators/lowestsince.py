"""
Lowest-Since Generator
======================

Generator for generating when a location has had the lowest amount of
recoveries or deaths since a particular date.
"""

from datetime import datetime

from covid19gng.constants import DF_DATE_FORMAT
from covid19gng.constants import REPORT_DATE_FORMAT
from covid19gng.generators import CountryAndStateGenerator

# Minimum number of days the previous date must be in order to get reported
DAYS_THRESHOLD = 30


class LowestSinceGenerator(CountryAndStateGenerator):
    """
    LowestSinceGenerator class. See module documentation for more information.
    """

    def __init__(self, df, data_desc=None):
        super().__init__(df)

        if data_desc is None:
            raise Exception("data_desc is required")

        self._data_desc = data_desc

    def _process_series(self, series, location):
        # Get daily values
        series = (series - series.shift(1))[1:]

        todays_value = series[-1]
        previous_date = None

        i = 1
        for date in series.index[-2::-1]:
            value = series[date]

            if value <= todays_value:
                if i >= DAYS_THRESHOLD and value >= 0:
                    previous_date = date
                break

            i += 1

        if previous_date is not None:
            text = "* **%s** \\- lowest %s since %s (%s)"

            previous_date = datetime.strptime(previous_date, DF_DATE_FORMAT)
            previous_date = previous_date.strftime(REPORT_DATE_FORMAT)

            print(text % (location, self._data_desc, previous_date, str(int(todays_value))))
            return True

        return False
