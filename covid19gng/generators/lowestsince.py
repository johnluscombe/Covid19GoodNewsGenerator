"""
Lowest-Since Generator
======================

Generator for generating when a location has had the lowest amount of
recoveries or deaths since a particular date.
"""

from datetime import datetime
from datetime import timedelta

from covid19gng.constants import EARLIEST
from covid19gng.constants import COUNTRY
from covid19gng.constants import STATE
from covid19gng.constants import PROVINCE
from covid19gng.constants import DF_DATE_FORMAT
from covid19gng.constants import REPORT_DATE_FORMAT
from covid19gng.generators import CountryAndStateGenerator
from covid19gng.utils import get_country_sum

# Latest the previous date must be in order to get reported
DATE_THRESHOLD = datetime.now() - timedelta(days=30)

# Earliest date as datetime object
EARLIEST_DATE = datetime.strptime(EARLIEST, DF_DATE_FORMAT)

# Earliest date as formatted object
EARLIEST_FORMATTED = EARLIEST_DATE.strftime(REPORT_DATE_FORMAT)


def process_series(series, location, data_desc):
    """
    Reports good news about the given location using the given
    :class:`~pandas.Series`.

    Args:
        series (:class:`~pandas.Series`): Series to use to report good
            news.
        location (str): Location to report good news about.
        data_desc (str): Description of the data being processed.
    """

    todays_value = series[-1]

    # Take out today's value from series
    series = series[:-1]

    candidates = series[series <= todays_value]

    if len(candidates) == 0:
        # Today's value is lowest in recorded history!
        print(f"* **{location}** \\- lowest {data_desc} "
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

        report = f"* **{location}** \\- lowest {data_desc} " \
                 f"since {previous_date} ({int(todays_value):,})"

        if earliest_date is not None:
            earliest_date = earliest_date.strftime(REPORT_DATE_FORMAT)
            report += f" (possibly as early as {earliest_date})"

        print(report)

        return True

    return False


class LowestSinceGenerator(CountryAndStateGenerator):
    """
    LowestSinceGenerator class. See module documentation for more information.

    Args:
        df (:class:`~pd.DataFrame`): :class:`~pd.DataFrame` to process.
        data_desc (str): Description of the data being processed.
    """

    def __init__(self, df, data_desc=None):
        super().__init__(df)

        if data_desc is None:
            raise Exception("data_desc is required")

        self._data_desc = data_desc

    def _process_series(self, series, location):
        # Get daily values
        series = (series - series.shift(1))[1:]

        return process_series(series, location, self._data_desc)


class ActiveCasesLowestSinceGenerator:
    """
    :class:`~LowestSinceGenerator` for active cases.

    Args:
        conf_df (:class:`~pd.DataFrame`): :class:`~pd.DataFrame` for confirmed
            cases.
        rec_df (:class:`~pd.DataFrame`): :class:`~pd.DataFrame` for recoveries.
    """

    def __init__(self, conf_df, rec_df):
        self._conf_df = conf_df
        self._rec_df = rec_df

    def generate(self):
        count = 0

        # Report countries
        if COUNTRY in self._rec_df.columns:
            # Global / not US
            conf_countries_df = self._conf_df.groupby(
                COUNTRY).apply(get_country_sum)

            rec_countries_df = self._rec_df.groupby(
                COUNTRY).apply(get_country_sum)

            for country in rec_countries_df.index:
                if country in conf_countries_df.index:
                    conf_country_series = conf_countries_df.loc[country]
                    rec_country_series = rec_countries_df.loc[country]
                    series = conf_country_series[EARLIEST:] - \
                        rec_country_series[EARLIEST:]

                    if self._process_series(series, country):
                        count += 1

        # Report states
        state_header = STATE if STATE in self._rec_df.columns else PROVINCE
        conf_states_df = self._conf_df.groupby(state_header).sum()
        rec_states_df = self._rec_df.groupby(state_header).sum()
        states = sorted(rec_states_df.index)

        for state in states:
            if state in conf_states_df.index:
                conf_state_series = conf_states_df.loc[state]
                rec_state_series = rec_states_df.loc[state]
                series = conf_state_series[EARLIEST:] - \
                    rec_state_series[EARLIEST:]

                if self._process_series(series, state):
                    count += 1

        return count

    def _process_series(self, series, location):
        """
        Reports good news about the given location using the given
        :class:`~pandas.Series`.

        Args:
            series (:class:`~pandas.Series`): Series to use to report good
                news.
            location (str): Location to report good news about.
        """

        return process_series(series, location, "active cases")
