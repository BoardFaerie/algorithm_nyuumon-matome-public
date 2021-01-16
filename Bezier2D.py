class Bezier2D:
    """Bezier curve class for a layer"""
    # https://ja.wikipedia.org/wiki/ベジェ曲線
    # https://en.wikipedia.org/wiki/Bézier_curve

    @staticmethod
    def quadratic_curve(layer:Layer, x0:int, y0:int, x1:int, y1:int, x2:int, y2:int, c, div=50):
        t = np.linspace(0, 1, div)
        x = ((1 - t) ** 2) * x0 + 2 * (1 - t) * t * x1 + (t ** 2) * x2
        y = ((1 - t) ** 2) * y0 + 2 * (1 - t) * t * y1 + (t ** 2) * y2
        layer.draw(x, y, c)

    @staticmethod
    def cubic_curve(layer:Layer, x0:int, y0:int, x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, c, div=50):
        t = np.linspace(0, 1, div)
        x = ((1 - t) ** 3) * x0 + 3 * ((1 - t) ** 2) * t * x1 + (1 - t) * (t ** 2) * x2 + (t ** 3) * x3
        y = ((1 - t) ** 3) * y0 + 3 * ((1 - t) ** 2) * t * y1 + (1 - t) * (t ** 2) * y2 + (t ** 3) * y3
        layer.draw(x, y, c)
