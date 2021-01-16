class Line2D:
    """Line class for a layer"""

    @staticmethod
    def vline(layer:Layer, x: int, y0: int, y1: int, c0=None, c1=None, z0=0, z1=0, n0=None, n1=None, lights=None, shadows=None):
        """Draw a vertical line from (x, y0) to (x, y1) with color c"""
        #print("vline: x: ", x, ", y0: ", y0, ", y1: ", y1, ", c0: ", c0, ", c1: ", c1, ", z0: ", z0, ", z1: ", z1, ", n0: ", n0, ", n1: ", n1, ", lights: ", lights, ", shadows: ", shadows)
        if y0 == y1:
            layer.draw_point(x, y0, c0, max([z0, z1]), n0, lights, shadows)
        else:
            if y0 > y1:
                y0, y1 = y1, y0
                z0, z1 = z1, z0
                if n0 is not None:
                    c0, c1 = c1.copy(), c0.copy()
                    n0, n1 = n1.copy(), n0.copy()

            if 0 <= x < layer.W:
                if 0 <= y1 and y0 < layer.H:
                    if y0 < 0:
                        z0 = z1 + (z0 - z1) * (0 - y1) / (y0 - y1)
                        if n0 is not None:
                            c0 = c1 + (c0 - c1) * (0 - y1) / (y0 - y1)
                            n0 = n1 + (n0 - n1) * (0 - y1) / (y0 - y1)
                        y0 = 0
                    if y0 == y1:
                        layer.draw_point(x, y0, c0, max([z0, z1]), n0, lights, shadows)
                    else:
                        if y1 >= layer.H:
                            z1 = z0 + (z1 - z0) * (layer.H - 1 - y0) / (y1 - y0)
                            if n0 is not None:
                                c1 = c0 + (c1 - c0) * (layer.H - 1 - y0) / (y1 - y0)
                                n1 = n0 + (n1 - n0) * (layer.H - 1 - y0) / (y1 - y0)
                            y1 = layer.H - 1
                        if y0 == y1:
                            layer.draw_point(x, y0, c0, max([z0, z1]), n0, lights, shadows)
                        else:
                            y = np.arange(y0, y1 + 1)
                            if n0 is not None:
                                layer.draw(np.full(y.size, x, dtype='i8'), y,
                                np.tile(c0.reshape(1, -1), (y.size, 1)) + np.tile((c1 - c0).reshape(1, -1), (y.size, 1)) * (np.tile(y.reshape(-1, 1), (1, c0.size)) - y0) / (y1 - y0),
                                np.full(y.size, z0) + np.full(y.size, z1 - z0) * (y - y0) / (y1 - y0),
                                np.tile(n0.reshape(1, -1), (y.size, 1)) + np.tile((n1 - n0).reshape(1, -1), (y.size, 1)) * (np.tile(y.reshape(-1, 1), (1, n0.size)) - y0) / (y1 - y0), lights, shadows)
                            else:
                                layer.draw(np.full(y.size, x, dtype='i8'), y, z=np.full(y.size, z0) + np.full(y.size, z1 - z0) * (y - y0) / (y1 - y0))

    @staticmethod
    def hline(layer:Layer, x0: int, x1: int, y: int, c0=None, c1=None, z0=0, z1=0, n0=None, n1=None, lights=None, shadows=None):
        """Draw a horizontal line from (x0, y) to (x1, y) with color c"""
        #print("hline: x0: ", x0, ", x1: ", x1, ", y: ", y, ", c0: ", c0, ", c1: ", c1, ", z0: ", z0, ", z1: ", z1, ", n0: ", n0, ", n1: ", n1, ", lights: ", lights, ", shadows: ", shadows)
        #print("hline: x0: ", x0, ", x1: ", x1, ", y: ", y, ", c0: ", c0, ", c1: ", c1, ", z0: ", z0, ", z1: ", z1, ", n0: ", n0, ", n1: ", n1)
        if x0 == x1:
            layer.draw_point(x0, y, c0, max([z0, z1]), n0, lights, shadows)
        else:
            if x0 > x1:
                x0, x1 = x1, x0
                z0, z1 = z1, z0
                if n0 is not None:
                    c0, c1 = c1.copy(), c0.copy()
                    n0, n1 = n1.copy(), n0.copy()

            if 0 <= y < layer.H:
                if 0 <= x1 and x0 < layer.W:
                    if x0 < 0:
                        z0 = z1 + (z0 - z1) * (0 - x1) / (x0 - x1)
                        if n0 is not None:
                            c0 = c1 + (c0 - c1) * (0 - x1) / (x0 - x1)
                            n0 = n1 + (n0 - n1) * (0 - x1) / (x0 - x1)
                        x0 = 0
                    if x0 == x1:
                        layer.draw_point(x0, y, c0, max([z0, z1]), n0, lights, shadows)
                    else:
                        if x1 >= layer.W:
                            z1 = z0 + (z1 - z0) * (layer.W - 1 - x0) / (x1 - x0)
                            if n0 is not None:
                                c1 = c0 + (c1 - c0) * (layer.W - 1 - x0) / (x1 - x0)
                                n1 = n0 + (n1 - n0) * (layer.W - 1 - x0) / (x1 - x0)
                            x1 = layer.W - 1
                        if x0 == x1:
                            layer.draw_point(x0, y, c0, max([z0, z1]), n0, lights, shadows)
                        else:
                            x = np.arange(x0, x1 + 1)
                            if n0 is not None:
                                layer.draw(x, np.full(x.size, y, dtype='i8'),
                                np.tile(c0.reshape(1, -1), (x.size, 1)) + np.tile((c1 - c0).reshape(1, -1), (x.size, 1)) * (np.tile(x.reshape(-1, 1), (1, c0.size)) - x0) / (x1 - x0),
                                np.full(x.size, z0) + np.full(x.size, z1 - z0) * (x - x0) / (x1 - x0),
                                np.tile(n0.reshape(1, -1), (x.size, 1)) + np.tile((n1 - n0).reshape(1, -1), (x.size, 1)) * (np.tile(x.reshape(-1, 1), (1, n0.size)) - x0) / (x1 - x0), lights, shadows)
                            else:
                                layer.draw(x, np.full(x.size, y, dtype='i8'), z=np.full(x.size, z0) + np.full(x.size, z1 - z0) * (x - x0) / (x1 - x0))

    @staticmethod
    def hline_triangle(layer:Layer, x0: int, x1: int, y: int, c0, c1, z0, z1, n0, n1):
        if x0 == x1:
            return np.array([x0], dtype='i8'), np.array([y], dtype='i8'), c0.reshape(1, -1), np.array([max([z0, z1])]), n0.reshape(1, -1)
        else:
            if x0 > x1:
                x0, x1 = x1, x0
                z0, z1 = z1, z0
                c0, c1 = c1.copy(), c0.copy()
                n0, n1 = n1.copy(), n0.copy()

            if 0 <= y < layer.H:
                if 0 <= x1 and x0 < layer.W:
                    if x0 < 0:
                        z0 = z1 + (z0 - z1) * (0 - x1) / (x0 - x1)
                        c0 = c1 + (c0 - c1) * (0 - x1) / (x0 - x1)
                        n0 = n1 + (n0 - n1) * (0 - x1) / (x0 - x1)
                        x0 = 0
                    if x0 == x1:
                        return np.array([x0], dtype='i8'), np.array([y], dtype='i8'), c0.reshape(1, -1), np.array([max([z0, z1])]), n0.reshape(1, -1)
                    else:
                        if x1 >= layer.W:
                            z1 = z0 + (z1 - z0) * (layer.W - 1 - x0) / (x1 - x0)
                            c1 = c0 + (c1 - c0) * (layer.W - 1 - x0) / (x1 - x0)
                            n1 = n0 + (n1 - n0) * (layer.W - 1 - x0) / (x1 - x0)
                            x1 = layer.W - 1
                        if x0 == x1:
                            return np.array([x0], dtype='i8'), np.array([y], dtype='i8'), c0.reshape(1, -1), np.array([max([z0, z1])]), n0.reshape(1, -1)
                        else:
                            x = np.arange(x0, x1 + 1, dtype='i8')
                            return x, np.full(x.size, y, dtype='i8'), np.tile(c0.reshape(1, -1), (x.size, 1)) + np.tile((c1 - c0).reshape(1, -1), (x.size, 1)) * (np.tile(x.reshape(-1, 1), (1, c0.size)) - x0) / (x1 - x0), np.full(x.size, z0) + np.full(x.size, z1 - z0) * (x - x0) / (x1 - x0), np.tile(n0.reshape(1, -1), (x.size, 1)) + np.tile((n1 - n0).reshape(1, -1), (x.size, 1)) * (np.tile(x.reshape(-1, 1), (1, n0.size)) - x0) / (x1 - x0)
                else:
                    return None, None, None, None, None
            else:
                return None, None, None, None, None

    @staticmethod
    def hline_triangle_shadow(layer:Layer, x0: int, x1: int, y: int, z0, z1):
        if x0 == x1:
            return np.array([x0], dtype='i8'), np.array([y], dtype='i8'), np.array([max([z0, z1])])
        else:
            if x0 > x1:
                x0, x1 = x1, x0
                z0, z1 = z1, z0

            if 0 <= y < layer.H:
                if 0 <= x1 and x0 < layer.W:
                    if x0 < 0:
                        z0 = z1 + (z0 - z1) * (0 - x1) / (x0 - x1)
                        x0 = 0
                    if x0 == x1:
                        return np.array([x0], dtype='i8'), np.array([y], dtype='i8'), np.array([max([z0, z1])])
                    else:
                        if x1 >= layer.W:
                            z1 = z0 + (z1 - z0) * (layer.W - 1 - x0) / (x1 - x0)
                            x1 = layer.W - 1
                        if x0 == x1:
                            return np.array([x0], dtype='i8'), np.array([y], dtype='i8'), np.array([max([z0, z1])])
                        else:
                            x = np.arange(x0, x1 + 1, dtype='i8')
                            return x, np.full(x.size, y, dtype='i8'), np.full(x.size, z0) + np.full(x.size, z1 - z0) * (x - x0) / (x1 - x0)
                else:
                    return None, None, None
            else:
                return None, None, None

    @staticmethod
    def line(layer:Layer, x0: int, y0: int, x1: int, y1: int, c0=None, c1=None, z0=0, z1=0, n0=None, n1=None, lights=None, shadows=None, antialias=False, wire_frame=False):
        """Draw a line from (x0, y0) to (x1, y1) with color c"""
        #print("line: x0: ", x0, ", y0: ", y0, ", x1: ", x1, ", y1: ", y1, ", c0: ", c0, ", c1: ", c1, ", z0: ", z0, ", z1: ", z1, ", n0: ", n0, ", n1: ", n1, ", lights: ", lights, ", shadows: ", shadows)
        if antialias:
            # Xiaolin Wu
            # https://en.wikipedia.org/wiki/Xiaolin_Wu%27s_line_algorithm

            steep = (abs(y1 - y0) > abs(x1 - x0))

            if steep:
                x0, y0 = y0, x0
                x1, y1 = y1, x1

            if x0 > x1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
                z0, z1 = z1, z0
                c0, c1 = c1.copy(), c0.copy()
                n0, n1 = n1.copy(), n0.copy()

            dx = x1 - x0
            dy = y1 - y0

            grad = 1 if dx == 0 else dy / dx

            xend = x0
            yend = y0 + grad * (xend - x0)
            xgap = 0.5
            xpxl1 = xend
            ypxl1 = Util.ipart(yend)

            if steep:
                layer.draw_point(ypxl1, xpxl1, np.clip(np.floor(c * (Util.rfpart(yend) * xgap)), 0, 255))
                layer.draw_point(ypxl1 + 1, xpxl1, np.clip(np.floor(c * (Util.fpart(yend) * xgap)), 0, 255))
            else:
                layer.draw_point(xpxl1, ypxl1, np.clip(np.floor(c * (Util.rfpart(yend) * xgap)), 0, 255))
                layer.draw_point(xpxl1, ypxl1 + 1, np.clip(np.floor(c * (Util.fpart(yend) * xgap)), 0, 255))

            intery = yend + grad

            xend = x1
            yend = y1 + grad * (xend - x1)
            xgap = 0.5
            xpxl2 = xend
            ypxl2 = Util.ipart(yend)

            if steep:
                layer.draw_point(ypxl2, xpxl2, np.clip(np.floor(c * (Util.rfpart(yend) * xgap)), 0, 255))
                layer.draw_point(ypxl2 + 1, xpxl2, np.clip(np.floor(c * (Util.fpart(yend) * xgap)), 0, 255))
            else:
                layer.draw_point(xpxl2, ypxl2, np.clip(np.floor(c * (Util.rfpart(yend) * xgap)), 0, 255))
                layer.draw_point(xpxl2, ypxl2 + 1, np.clip(np.floor(c * (Util.fpart(yend) * xgap)), 0, 255))

            if steep:
                for x in range(xpxl1 + 1, xpxl2):
                    layer.draw_point(Util.ipart(intery), x, np.clip(np.floor(c * Util.rfpart(intery)), 0, 255))
                    layer.draw_point(Util.ipart(intery) + 1, x, np.clip(np.floor(c * Util.fpart(intery)), 0, 255))
                    intery += grad
            else:
                for x in range(xpxl1 + 1, xpxl2):
                    layer.draw_point(x, Util.ipart(intery), np.clip(np.floor(c * Util.rfpart(intery)), 0, 255))
                    layer.draw_point(x, Util.ipart(intery) + 1, np.clip(np.floor(c * Util.fpart(intery)), 0, 255))
                    intery += grad
        else:
            # Bresenham
            # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm

            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy
            x = x0
            y = y0

            if n0 is not None:
                while True:
                    layer.draw_point(x, y, c0 + (c1 - c0) * (x - x0) / (x1 - x0), z0 + (z1 - z0) * (x - x0) / (x1 - x0), n0 + (n1 - n0) * (x - x0) / (x1 - x0), lights, shadows, wire_frame)

                    if x == x1 and y == y1:
                        break

                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x += sx
                    if e2 < dx:
                        err += dx
                        y += sy
            else:
                while True:
                    layer.draw_point(x, y, z=z0 + (z1 - z0) * (x - x0) / (x1 - x0))

                    if x == x1 and y == y1:
                        break

                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x += sx
                    if e2 < dx:
                        err += dx
                        y += sy
