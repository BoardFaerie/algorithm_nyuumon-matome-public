class Polygon2D:
    """(Regular) Polygon class for a layer"""

    @staticmethod
    def regular_polygon(layer:Layer, x, y, r, n, c, antialias=False):
        """Draw a regular polygon with center (x, y), radius r, division n, color c"""
        for i in range(n):
            Line2D.line(layer, round(x + r * np.cos(2 * np.pi * i / n)), round(y + r * np.sin(2 * np.pi * i / n)), round(x + r * np.cos(2 * np.pi * (i + 1) / n)), round(y + r * np.sin(2 * np.pi * (i + 1) / n)), c, c)

    @staticmethod
    def filled_regular_polygon(layer:Layer, x, y, r, n, c, antialias=False):
        """Draw a filled regular polygon with center (x, y), radius r, division n, color c"""
        for i in range(n):
            Triangle2D.filled_triangle(layer, round(x), round(y), round(x + r * np.cos(2 * np.pi * i / n)), round(y + r * np.sin(2 * np.pi * i / n)), round(x + r * np.cos(2 * np.pi * (i + 1) / n)), round(y + r * np.sin(2 * np.pi * (i + 1) / n)), c, c, c)
