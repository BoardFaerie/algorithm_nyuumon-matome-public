class Rectangle2D:
    """Rectangle class for a layer"""

    @staticmethod
    def rectangle(layer:Layer, x0: int, y0: int, x1: int, y1: int, t: int, c, antialias=False):
        """Draw a rectangle of (x0, y0), (x0, y1), (x1, y0), (x1, y1) with line thickness t and color c"""
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0

        if x0 == x1:
            Line2D.vline(layer, x0, y0, y1, c, c)
            return
        if y0 == y1:
            Line2D.hline(layer, x0, x1, y0, c, c)
            return

        if 2 * t > x1 - x0 + 1:
            t = round((x1 - x0 - 1) / 2)
        if 2 * t > y1 - y0 + 1:
            t = round((y1 - y0 - 1) / 2)

        for i in range(t):
            Line2D.vline(layer, x0 + i, y0, y1, c, c)
            Line2D.vline(layer, x1 - i, y0, y1, c, c)
            Line2D.hline(layer, x0, x1, y0 + i, c, c)
            Line2D.hline(layer, x0, x1, y1 - i, c, c)

    @staticmethod
    def filled_rectangle(layer:Layer, x0: int, y0: int, x1: int, y1: int, c, antialias=False):
        """Draw a filled rectangle of (x0, y0), (x0, y1), (x1, y0), (x1, y1) with color c"""
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0

        for i in range(x0, x1 + 1):
            Line2D.vline(layer, i, y0, y1, c, c)
