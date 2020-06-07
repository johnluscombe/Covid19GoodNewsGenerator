"""
COVID-19 Good News Generator
============================

Module for reporting good news, based on data, about the novel coronavirus in
various locations. The data comes from John Hopkins University:
https://github.com/CSSEGISandData/COVID-19
"""

import argparse

from datetime import datetime
import pandas as pd

from covid19gng.constants import DF_DATE_FORMAT
from covid19gng.constants import COUNTRY
from covid19gng.constants import GLOBAL
from covid19gng.constants import US
from covid19gng.constants import CONFIRMED
from covid19gng.constants import DEATHS
from covid19gng.constants import RECOVERED
from covid19gng.generators import LowestSinceGenerator
from covid19gng.generators import ActiveCasesLowestSinceGenerator
from covid19gng.generators import RecoveryMilestoneGenerator
from covid19gng.utils import input_and_validate

BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
           "/csse_covid_19_time_series/time_series_covid19_%s_%s.csv "


class AppRunner:
    def __init__(self, args):
        print("Loading...")
        self.global_confirmed_df = pd.read_csv(BASE_URL % (CONFIRMED, GLOBAL))
        self.global_deaths_df = pd.read_csv(BASE_URL % (DEATHS, GLOBAL))
        self.global_recoveries_df = pd.read_csv(BASE_URL % (RECOVERED, GLOBAL))
        self.us_confirmed_df = pd.read_csv(BASE_URL % (CONFIRMED, US))
        self.us_deaths_df = pd.read_csv(BASE_URL % (DEATHS, US))

        self.args = args

        dates = []

        for df in [self.global_confirmed_df, self.global_deaths_df,
                   self.global_recoveries_df, self.us_confirmed_df,
                   self.us_deaths_df]:

            dates.append(datetime.strptime(df.columns[-1], DF_DATE_FORMAT))

        print("Last Updated: %s" % max(dates).strftime(DF_DATE_FORMAT))

    def run(self):
        loop = True

        while loop:
            confirmed_df = self.global_confirmed_df
            deaths_df = self.global_deaths_df
            recoveries_df = self.global_recoveries_df

            country = self.args.country

            # Prompt user for country
            if country is None:
                country = self._prompt_for_country(confirmed_df)
            else:
                if country.lower() == "none":
                    # If the country flag is "none", treat it as if the user
                    # entered nothing for the country
                    country = ""

                loop = False

            if country:
                confirmed_df = confirmed_df[confirmed_df[COUNTRY] == country]
                deaths_df = deaths_df[deaths_df[COUNTRY] == country]
                recoveries_df = recoveries_df[recoveries_df[COUNTRY] == country]

            self._report_confirmed_cases_milestones(country, confirmed_df)
            self._report_active_cases_milestones(confirmed_df, recoveries_df)
            self._report_deaths_milestones(country, deaths_df)
            self._report_recoveries_milestones(recoveries_df)

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

    def _report_confirmed_cases_milestones(self, country, df):
        print("\nConfirmed cases milestones:\n")

        data_desc = "confirmed cases"

        us_news_to_report = False
        if not country or country == US:
            gen = LowestSinceGenerator(self.us_confirmed_df, data_desc)
            us_news_to_report = gen.generate()

        gen = LowestSinceGenerator(df, data_desc)
        global_news_to_report = gen.generate()

        if not us_news_to_report and not global_news_to_report:
            print("No news to report.")

    def _report_active_cases_milestones(self, conf_df, rec_df):
        print("\nActive cases milestones:\n")

        gen = ActiveCasesLowestSinceGenerator(conf_df, rec_df)

        if not gen.generate():
            print("No news to report.")

    def _report_deaths_milestones(self, country, global_df):
        print("\nDeaths milestones:\n")

        data_desc = "deaths"

        us_news_to_report = False
        if not country or country == US:
            gen = LowestSinceGenerator(self.us_deaths_df, data_desc)
            us_news_to_report = gen.generate()

        gen = LowestSinceGenerator(global_df, data_desc)
        global_news_to_report = gen.generate()

        if not us_news_to_report and not global_news_to_report:
            print("No news to report.")

    def _report_recoveries_milestones(self, df):
        print("\nRecoveries milestones:\n")

        gen = RecoveryMilestoneGenerator(df)

        if not gen.generate():
            print("No news to report.")


if __name__ == "__main__":
    description = "Reports good news, based on data, about the novel " \
                  "coronavirus in various locations"

    help = "Country to report good news about. Use 'None' to view good news " \
           "about all countries."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--country", help=help)

    plotter = AppRunner(parser.parse_args())
    plotter.run()
