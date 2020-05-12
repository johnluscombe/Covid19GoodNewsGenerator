"""
Covid19Plotter
==============

Module for plotting trends about the novel coronavirus in various locations.
The data comes from John Hopkins University:
https://github.com/CSSEGISandData/COVID-19
"""

from datetime import datetime
import pandas as pd

from covid19gng.aliases import STATE_ABBREVIATIONS
from covid19gng.constants import COUNTRY
from covid19gng.constants import STATE
from covid19gng.constants import PROVINCE
from covid19gng.generators import LowestSinceGenerator
from covid19gng.utils import input_and_validate

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
           "/csse_covid_19_time_series/time_series_covid19_%s_%s.csv "

DATE_FORMAT = "%m/%d/%y"

GLOBAL = "global"
US = "US"

CONFIRMED = "confirmed"
DEATHS = "deaths"
RECOVERED = "recovered"


class AppRunner:
    def __init__(self):
        print("Loading...")
        self.global_confirmed_df = pd.read_csv(BASE_URL % (CONFIRMED, GLOBAL))
        self.global_deaths_df = pd.read_csv(BASE_URL % (DEATHS, GLOBAL))
        self.global_recoveries_df = pd.read_csv(BASE_URL % (RECOVERED, GLOBAL))
        self.us_confirmed_df = pd.read_csv(BASE_URL % (CONFIRMED, US))
        self.us_deaths_df = pd.read_csv(BASE_URL % (DEATHS, US))

        dates = []

        for df in [self.global_confirmed_df, self.global_deaths_df,
                   self.global_recoveries_df, self.us_confirmed_df,
                   self.us_deaths_df]:

            dates.append(datetime.strptime(df.columns[-1], DATE_FORMAT))

        print("Last Updated: %s\n" % max(dates).strftime(DATE_FORMAT))

    def run(self):
        while True:
            confirmed_df = self.global_confirmed_df
            deaths_df = self.global_deaths_df
            recoveries_df = self.global_recoveries_df

            # Prompt user for country
            country = self._prompt_for_country(confirmed_df)
            state = None

            if country == US:
                confirmed_df = self.us_confirmed_df
                deaths_df = self.us_deaths_df
                state_header = STATE
            else:
                confirmed_df = self._filter_df(confirmed_df, COUNTRY, country)
                deaths_df = self._filter_df(deaths_df, COUNTRY, country)
                recoveries_df = self._filter_df(recoveries_df, COUNTRY, country)
                state_header = PROVINCE

            if len(confirmed_df) > 1:
                state = self._prompt_for_state(confirmed_df, country)

            confirmed_df = self._filter_df(confirmed_df, state_header, state)
            deaths_df = self._filter_df(deaths_df, state_header, state)

            generators = [
                LowestSinceGenerator(confirmed_df, "confirmed cases"),
                LowestSinceGenerator(deaths_df, "deaths")
            ]

            count = 0
            for generator in generators:
                count += generator.generate()

            if count == 0:
                print("No news to report.")

    def _prompt_for_country(self, global_df):
        """
        Gets the desired country/region from the user.

        Args:
            global_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for non-US
                countries.

        Returns:
            str
        """

        prompt = "Which country/region do you want to view? (Type OPTIONS to " \
                 "see all available options)"

        return input_and_validate(
            prompt=prompt, options=global_df[COUNTRY].tolist())

    def _prompt_for_state(self, country_df, country):
        """
        Gets the desired state from the user.

        Args:
            country_df (:class:`~pd.DataFrame`): `~pd.DataFrame` for the entire
                country.
            country (str): Country specified by the user.

        Returns:
            str
        """

        prompt = "Which state/province do you want to view? (Just press ENTER " \
                 "to see all states, or type OPTIONS to see all available options)"

        ignore = [""]

        if country == US:
            ignore += list(STATE_ABBREVIATIONS.keys())
            state_df = country_df[STATE]
        else:
            state_df = country_df[PROVINCE]

        state = input_and_validate(prompt=prompt, options=state_df.tolist(),
                                   ignore=ignore)

        state_upper = state.upper()
        if state_upper in STATE_ABBREVIATIONS:
            state = STATE_ABBREVIATIONS[state_upper]

        return state

    def _filter_df(self, df, key, value):
        """
        Filters the given :class:`~pd.DataFrame` using the given filter key and
        values.

        Args:
            df (:class:`~pd.DataFrame`): :class:`~pd.DataFrame` to filter.
            key (str): Filter key.
            values (str or list): Filter values.

        Returns:
            :class:`~pd.DataFrame`
        """

        if not value:
            nan_df = df[key].isna()

            if nan_df.sum() == 1:
                # If a row exists in the filtered data frame where the value of
                # the given key is NaN, it is the total row, so use that for
                # the data
                df = df[nan_df]
        else:
            if type(value) != list:
                value = [value]

            df = df[df[key].isin(value)]

        return df


if __name__ == "__main__":
    plotter = AppRunner()
    plotter.run()
