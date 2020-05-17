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
        yesterday, today = series[-2:]
        today_num_digits = len(str(int(today)))
        remainder_multiple = 10 ** (today_num_digits - 1)

        if today > RECOVERIES_THRESHOLD:
            milestone = int(today / remainder_multiple) * remainder_multiple

            if today > milestone >= yesterday:
                text = "%s passed %s recoveries (%s)"
                print(text % (location, milestone, today))
