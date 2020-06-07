"""
Country and State Generator
===========================

Generator for generating good news for all countries and states in a given
data frame.
"""

from covid19gng.constants import EARLIEST
from covid19gng.constants import COUNTRY
from covid19gng.constants import STATE
from covid19gng.constants import PROVINCE
from covid19gng.generators import GeneratorBase
from covid19gng.utils import get_country_sum


class CountryAndStateGenerator(GeneratorBase):
    """
    CountryAndStateGenerator class. See module documentation for more
    information.
    """

    def generate(self):
        count = 0

        # Report countries
        if COUNTRY in self._df.columns:
            # Global / not US
            countries_df = self._df.groupby(COUNTRY).apply(get_country_sum)
            for i in range(len(countries_df)):
                country_series = countries_df.iloc[i]
                if self._process_series(country_series[EARLIEST:], country_series[COUNTRY]):
                    count += 1

        # Report states
        state_header = STATE if STATE in self._df.columns else PROVINCE
        state_df = self._df.groupby(state_header).sum()
        states = sorted(state_df.index)

        for state in states:
            if self._process_series(state_df.loc[state][EARLIEST:], state):
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

        pass
