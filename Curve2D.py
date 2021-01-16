class Curve2D:
    """Curve class for a layer"""

    @staticmethod
    def thick_line_with_circles(layer:Layer, x0: int, y0: int, x1: int, y1: int, t: int, c, antialias=False):
        """Draw a line from (x0, y0) to (x1, y1) with width t and color c, using circles"""
        if x0 == x1:
            for y in range(y0, y1 + 1):
                Circle2D.filled_circle(layer, x0, y, t, c, antialias)
            return
        if y0 == y1:
            for x in range(x0, x1 + 1):
                Circle2D.filled_circle(layer, x, y0, t, c, antialias)
            return

        slope = (y1 - y0) / (x1 - x0)

        if x0 < x1:
            for x in range(x0, x1 + 1):
                y = y0 + slope * (x - x0)
                Circle2D.filled_circle(layer, x, round(y), t, c, antialias)
        else:
            for x in range(x1, x0 + 1):
                y = y0 + slope * (x - x0)
                Circle2D.filled_circle(layer, x, round(y), t, c, antialias)

        slope = (x1 - x0) / (y0 - y1)

        if y0 < y1:
            for y in range(y0, y1 + 1):
                x = x0 + slope * (y - y0)
                Circle2D.filled_circle(layer, round(x), y, t, c, antialias)
        else:
            for y in range(y1, y0 + 1):
                x = x0 + slope * (y - y0)
                Circle2D.filled_circle(layer, round(x), y, t, c, antialias)

    @staticmethod
    def circles_along_points(layer:Layer, points, r: int, c, antialias=False):
        """Draw a curve along points with circle of radius r and color c"""
        for point in points:
            Circle2D.filled_circle(layer, point[0], point[1], r, c, antialias)
