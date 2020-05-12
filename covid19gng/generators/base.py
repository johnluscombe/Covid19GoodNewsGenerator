"""
GeneratorBase
=============

Base functionlity for all good news generators.
"""

# First day data was collected
EARLIEST = "1/22/20"


class GeneratorBase:
    """
    GeneratorBase class. See module documentation for more information.
    """

    def __init__(self, df, **kwargs):
        self._df = df

    def generate(self):
        """
        Generates the good news output.

        Returns:
            int
        """

        return 0
