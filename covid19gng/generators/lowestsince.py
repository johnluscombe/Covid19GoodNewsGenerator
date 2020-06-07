"""
Lowest-Since Generator
======================

Generator for generating when a location has had the lowest amount of
recoveries or deaths since a particular date.
"""

from datetime import datetime
from datetime import timedelta

from covid19gng.constants import EARLIEST
from covid19gng.constants import DF_DATE_FORMAT
from covid19gng.constants import REPORT_DATE_FORMAT
from covid19gng.generators import CountryAndStateGenerator

# Latest the previous date must be in order to get reported
DATE_THRESHOLD = datetime.now() - timedelta(days=30)

# Earliest date as datetime object
EARLIEST = datetime.strptime(EARLIEST, DF_DATE_FORMAT)

# Earliest date as formatted object
EARLIEST_FORMATTED = EARLIEST.strftime(REPORT_DATE_FORMAT)


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

        # Take out today's value from series
        series = series[:-1]

        candidates = series[series <= todays_value]

        if len(candidates) == 0:
            # Today's value is lowest in recorded history!
            print(f"* **{location}** \\- lowest {self._data_desc} "
                  f"since before {EARLIEST_FORMATTED} ({int(todays_value):,})")

            return True

        previous_date_str = candidates.index[-1]
        previous_date = datetime.strptime(previous_date_str, DF_DATE_FORMAT)
        previous_value = candidates[-1]

        earliest_date = None

        if previous_value <= 0:
            # Any value less than or equal to 0 may not be reliable, so look
            # for a potential earlier date
            earlier_candidates = candidates[candidates > 0]

            if len(earlier_candidates) > 0:
                earliest_date_str = earlier_candidates.index[-1]
                earliest_date = datetime.strptime(earliest_date_str, DF_DATE_FORMAT)

        do_report = (previous_date is not None and
                     previous_date <= DATE_THRESHOLD) or \
                    (earliest_date is not None and
                     earliest_date <= DATE_THRESHOLD)

        if do_report:
            previous_date = previous_date.strftime(REPORT_DATE_FORMAT)

            report = f"* **{location}** \\- lowest {self._data_desc} " \
                     f"since {previous_date} ({int(todays_value):,})"

            if earliest_date is not None:
                earliest_date = earliest_date.strftime(REPORT_DATE_FORMAT)
                report += f" (possibly as early as {earliest_date})"

            print(report)

            return True

        return False
