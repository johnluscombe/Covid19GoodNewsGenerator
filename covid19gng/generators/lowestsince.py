from covid19gng.constants import EARLIEST
from covid19gng.constants import COUNTRY
from covid19gng.constants import STATE
from covid19gng.constants import PROVINCE
from covid19gng.generators import GeneratorBase

# Minimum number of days the previous date must be in order to get reported
DAYS_THRESHOLD = 30


class LowestSinceGenerator(GeneratorBase):
    def __init__(self, df, data_desc=None):
        super().__init__(df)

        if data_desc is None:
            raise Exception("data_desc is required")

        self._data_desc = data_desc

    def generate(self):
        count = 0

        state_header = STATE if STATE in self._df.columns else PROVINCE

        if len(self._df) > 1:
            self._df = self._df.groupby(state_header).sum()
        else:
            self._df = self._df.set_index(COUNTRY)

        for location in self._df.index:
            series = self._df.loc[location][EARLIEST:]

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
                text = "%s had its lowest %s since %s (%s)"
                print(text % (location, self._data_desc, previous_date, str(int(todays_value))))
                count += 1

        return count
