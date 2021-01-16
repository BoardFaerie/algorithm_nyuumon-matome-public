class Util:
    """Utility class for application"""

    @staticmethod
    def ipart(x):
        """integer part of x"""
        return np.floor(x)

    @staticmethod
    def fpart(x):
        """fraction part of x"""
        return x - np.floor(x)

    @staticmethod
    def rfpart(x):
        """1 minus fraction part of x"""
        return 1 - Util.fpart(x)

    @staticmethod
    def interpolate(x0, y0, x1, y1):
        if x0 == x1:
            return np.array([y0])
        else:
            return np.linspace(y0, y1, x1 - x0, dtype=int)
