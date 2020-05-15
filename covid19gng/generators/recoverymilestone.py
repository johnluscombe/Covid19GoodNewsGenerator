"""
Recovery Milestone
==================

Generator for generating when a location has passed a particular recovery
milestone.
"""

from covid19gng.generators import CountryAndStateGenerator

# Minimum number of recoveries in order to get reported
RECOVERIES_THRESHOLD = 1000


class RecoveryMilestoneGenerator(CountryAndStateGenerator):
    """
    RecoveryMilestoneGenerator class. See module documentation for more
    information.
    """

    def _process_series(self, series, location):
        yesterday_num_digits = len(str(int(series[-2])))
        today_num_digits = len(str(int(series[-1])))

        if today_num_digits > yesterday_num_digits and\
                series[-1] > RECOVERIES_THRESHOLD:

            milestone = "1" + ("0" * (today_num_digits - 1))
            text = "%s passed %s recoveries (%s)"
            print(text % (location, milestone, series[-1]))
