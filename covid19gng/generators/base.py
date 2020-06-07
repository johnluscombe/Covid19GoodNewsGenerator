"""
GeneratorBase
=============

Base functionlity for all good news generators.
"""


class GeneratorBase:
    """
    GeneratorBase class. See module documentation for more information.

    Args:
        :class:`~pd.DataFrame`: :class:`~pd.DataFrame to process.
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
