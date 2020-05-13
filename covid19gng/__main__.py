"""
Covid19Plotter
==============

Module for plotting trends about the novel coronavirus in various locations.
The data comes from John Hopkins University:
https://github.com/CSSEGISandData/COVID-19
"""

from datetime import datetime
import pandas as pd

from covid19gng.constants import DATE_FORMAT
from covid19gng.constants import COUNTRY
from covid19gng.constants import GLOBAL
from covid19gng.constants import US
from covid19gng.constants import CONFIRMED
from covid19gng.constants import DEATHS
from covid19gng.constants import RECOVERED
from covid19gng.generators import LowestSinceGenerator
from covid19gng.generators import RecoveryMilestoneGenerator
from covid19gng.utils import filter_df
from covid19gng.utils import input_and_validate

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
           "/csse_covid_19_time_series/time_series_covid19_%s_%s.csv "


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

            generators = []

            if not country or country == US:
                generators.extend([
                    LowestSinceGenerator(self.us_confirmed_df, "confirmed cases"),
                    LowestSinceGenerator(self.us_deaths_df, "deaths")
                ])

            if country:
                confirmed_df = filter_df(confirmed_df, COUNTRY, country)
                deaths_df = filter_df(deaths_df, COUNTRY, country)
                recoveries_df = filter_df(recoveries_df, COUNTRY, country)

            generators.extend([
                LowestSinceGenerator(confirmed_df, "confirmed cases"),
                LowestSinceGenerator(deaths_df, "deaths"),
                RecoveryMilestoneGenerator(recoveries_df)
            ])

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

        prompt = "Which country do you want to view? (Type OPTIONS to " \
                 "see all available options)"

        return input_and_validate(
            prompt=prompt, options=global_df[COUNTRY].tolist(), ignore=[""])


if __name__ == "__main__":
    plotter = AppRunner()
    plotter.run()
