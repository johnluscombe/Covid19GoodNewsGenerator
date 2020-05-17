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
        yesterdays_value, todays_value = series[-2:]
        today_num_digits = len(str(int(todays_value)))
        remainder_multiple = 10 ** (today_num_digits - 1)

        if todays_value > RECOVERIES_THRESHOLD:
            milestone = int(todays_value / remainder_multiple) * remainder_multiple

            if todays_value > milestone >= yesterdays_value:
                print(f"* **{location}** \\- passed {milestone:,} "
                      f"recoveries ({todays_value:,})")

                return True

        return False
