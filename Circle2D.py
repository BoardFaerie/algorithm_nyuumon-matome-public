class Circle2D:
    """Circle class for a layer"""

    RADIUS_MAX = 500
    D = np.zeros((RADIUS_MAX, np.ceil(np.sqrt(2) * RADIUS_MAX * RADIUS_MAX / 4).astype('i8') + 1))
    Dinit = False

    @classmethod
    def circle(cls, layer:Layer, cx: int, cy: int, r: int, c, antialias=False):
        """Draw a circle with center (cx, cy), radius r, and color c"""
        if antialias:
            # Xiaolin Wu
            # https://pieceofnostalgia-bd472.firebaseapp.com/java/anti_aliased_circle_algorithm.html
            if not cls.Dinit:
                for rdash in range(1, cls.RADIUS_MAX):
                    for y in range(1, np.ceil(rdash / np.sqrt(2)) + 1):
                        xt = np.sqrt(rdash * rdash - y * y)
                        cls.D[rdash, y] = np.ceil(xt) - xt
                cls.Dinit = True

            if r < cls.RADIUS_MAX:
                x = r
                y = 0
                d = 0
                d_old = 0
                layer.draw_point(cx + x, cy + y, c, c)
                layer.draw_point(cx - x, cy + y, c, c)
                layer.draw_point(cx + x, cy - y, c, c)
                layer.draw_point(cx - x, cy - y, c, c)

                while y < x - 1:
                    y += 1
                    d = cls.D[r, y]
                    if d < d_old:
                        x -= 1

                    ctmp1 = np.clip(np.floor(c * (1 - d)), 0, 255)
                    ctmp2 = np.clip(np.floor(c * d), 0, 255)
                    layer.draw_point(cx + x, cy + y, ctmp1, ctmp1)
                    layer.draw_point(cx - x, cy + y, ctmp1, ctmp1)
                    layer.draw_point(cx + x, cy - y, ctmp1, ctmp1)
                    layer.draw_point(cx - x, cy - y, ctmp1, ctmp1)
                    layer.draw_point(cx + y, cy + x, ctmp1, ctmp1)
                    layer.draw_point(cx - y, cy + x, ctmp1, ctmp1)
                    layer.draw_point(cx + y, cy - x, ctmp1, ctmp1)
                    layer.draw_point(cx - y, cy - x, ctmp1, ctmp1)
                    layer.draw_point(cx + x - 1, cy + y, ctmp2, ctmp2)
                    layer.draw_point(cx - x - 1, cy + y, ctmp2, ctmp2)
                    layer.draw_point(cx + x - 1, cy - y, ctmp2, ctmp2)
                    layer.draw_point(cx - x - 1, cy - y, ctmp2, ctmp2)
                    layer.draw_point(cx + y - 1, cy + x, ctmp2, ctmp2)
                    layer.draw_point(cx - y - 1, cy + x, ctmp2, ctmp2)
                    layer.draw_point(cx + y - 1, cy - x, ctmp2, ctmp2)
                    layer.draw_point(cx - y - 1, cy - x, ctmp2, ctmp2)
                    d_old = d
            else:
                darr = np.zeros(np.ceil(np.sqrt(2) * r * r / 4) + 1)
                for y in range(1, np.ceil(r / np.sqrt(2)) + 0.1):
                    xt = np.sqrt(r * r - y * y)
                    darr[y] = np.ceil(xt) - xt

                x = r
                y = 0
                d = 0
                d_old = 0
                layer.draw_point(cx + x, cy + y, c, c)
                layer.draw_point(cx - x, cy + y, c, c)
                layer.draw_point(cx + x, cy - y, c, c)
                layer.draw_point(cx - x, cy - y, c, c)

                while y < x - 1:
                    y += 1
                    d = darr[y]
                    if d < d_old:
                        x -= 1

                    ctmp1 = np.clip(np.floor(c * (1 - d)), 0, 255)
                    ctmp2 = np.clip(np.floor(c * d), 0, 255)
                    layer.draw_point(cx + x, cy + y, ctmp1, ctmp1)
                    layer.draw_point(cx - x, cy + y, ctmp1, ctmp1)
                    layer.draw_point(cx + x, cy - y, ctmp1, ctmp1)
                    layer.draw_point(cx - x, cy - y, ctmp1, ctmp1)
                    layer.draw_point(cx + y, cy + x, ctmp1, ctmp1)
                    layer.draw_point(cx - y, cy + x, ctmp1, ctmp1)
                    layer.draw_point(cx + y, cy - x, ctmp1, ctmp1)
                    layer.draw_point(cx - y, cy - x, ctmp1, ctmp1)
                    layer.draw_point(cx + x - 1, cy + y, ctmp2, ctmp2)
                    layer.draw_point(cx - x - 1, cy + y, ctmp2, ctmp2)
                    layer.draw_point(cx + x - 1, cy - y, ctmp2, ctmp2)
                    layer.draw_point(cx - x - 1, cy - y, ctmp2, ctmp2)
                    layer.draw_point(cx + y - 1, cy + x, ctmp2, ctmp2)
                    layer.draw_point(cx - y - 1, cy + x, ctmp2, ctmp2)
                    layer.draw_point(cx + y - 1, cy - x, ctmp2, ctmp2)
                    layer.draw_point(cx - y - 1, cy - x, ctmp2, ctmp2)
                    d_old = d
        else:
            # mid-point circle drawing algorithm
            # https://www.geeksforgeeks.org/mid-point-circle-drawing-algorithm/?ref=lbp
            if r == 0:
                layer.draw_point(cx, cy, c, c)
                return
            if r < 0:
                r = -r

            layer.draw_point(cx + r, cy, c, c)
            layer.draw_point(cx - r, cy, c, c)
            layer.draw_point(cx, cy + r, c, c)
            layer.draw_point(cx, cy - r, c, c)

            x = r
            y = 0
            P = 1 - r

            while x > y:
                y += 1
                if P <= 0:
                    P += 2 * y + 1
                else:
                    x -= 1
                    P += 2 * y - 2 * x + 1

                if x < y:
                    break

                layer.draw_point(cx + x, cy + y, c, c)
                layer.draw_point(cx - x, cy + y, c, c)
                layer.draw_point(cx + x, cy - y, c, c)
                layer.draw_point(cx - x, cy - y, c, c)

                if x != y:
                    layer.draw_point(cx + y, cy + x, c, c)
                    layer.draw_point(cx - y, cy + x, c, c)
                    layer.draw_point(cx + y, cy - x, c, c)
                    layer.draw_point(cx - y, cy - x, c, c)

    @staticmethod
    def ellipse(layer:Layer, cx: int, cy: int, rx: int, ry: int, c, antialias=False):
        """Draw an ellipse with center (cx, cy), radius (rx, ry), and color c"""
        # https://www.geeksforgeeks.org/midpoint-ellipse-drawing-algorithm/?ref=lbp
        if rx == 0 and ry == 0:
            layer.draw_point(cx, cy, c, c)
            return
        if rx == 0:
            Line2D.vline(layer, cx, cy - ry, cy + ry, c, c)
            return
        if ry == 0:
            Line2D.hline(layer, cx - ry, cx + ry, cy, c, c)
            return
        if rx < 0:
            rx = -rx
        if ry < 0:
            ry = -ry

        x = 0
        y = ry
        d1 = (ry * ry) - (rx * rx * ry) + (rx * rx / 4)
        dx = 2 * ry * ry * x
        dy = 2 * rx * rx * y

        while dx < dy:
            layer.draw_point(cx + x, cy + y, c, c)
            layer.draw_point(cx - x, cy + y, c, c)
            layer.draw_point(cx + x, cy - y, c, c)
            layer.draw_point(cx - x, cy - y, c, c)

            if d1 < 0:
                x += 1
                dx += 2 * ry * ry
                d1 += dx + ry * ry
            else:
                x += 1
                y -= 1
                dx += 2 * ry * ry
                dy -= 2 * rx * rx
                d1 += dx - dy + ry * ry

        d2 = ry * ry * (x + 0.5) * (x + 0.5) + rx * rx * (y - 1) * (y - 1) - rx * rx * ry * ry

        while y >= 0:
            layer.draw_point(cx + x, cy + y, c, c)
            layer.draw_point(cx - x, cy + y, c, c)
            layer.draw_point(cx + x, cy - y, c, c)
            layer.draw_point(cx - x, cy - y, c, c)

            if d2 > 0:
                y -= 1
                dy -= 2 * rx * rx
                d2 += rx * rx - dy
            else:
                y -= 1
                x += 1
                dx += 2 * ry * ry
                dy -= 2 * rx * rx
                d2 += dx - dy + rx * rx

    @staticmethod
    def filled_circle(layer:Layer, cx: int, cy: int, r: int, c, antialias=False):
        """Draw a filled circle with center (cx, cy), radius r, and color c"""
        if r == 0:
            layer.draw_point(cx, cy, c, c)
            return
        if r < 0:
            r = -r

        Line2D.hline(layer, cx - r, cx + r, cy, c, c)

        x = r
        y = 0
        P = 1 - r

        while x > y:
            y += 1
            if P <= 0:
                P += 2 * y + 1
            else:
                x -= 1
                P += 2 * y - 2 * x + 1

            if x < y:
                break

            Line2D.hline(layer, cx - x, cx + x, cy + y, c, c)
            Line2D.hline(layer, cx - x, cx + x, cy - y, c, c)

            if x != y:
                Line2D.hline(layer, cx - y, cx + y, cy + x, c, c)
                Line2D.hline(layer, cx - y, cx + y, cy - x, c, c)

    @staticmethod
    def filled_ellipse(layer:Layer, cx: int, cy: int, rx: int, ry: int, c, antialias=False):
        """Draw a filled ellipse with center (cx, cy), radius (rx, ry), and color c"""
        if rx == 0 and ry == 0:
            layer.draw_point(cx, cy, c, c)
            return
        if rx == 0:
            Line2D.vline(layer, cx, cy - ry, cy + ry, c, c)
            return
        if ry == 0:
            Line2D.hline(layer, cx - ry, cx + ry, cy, c, c)
            return
        if rx < 0:
            rx = -rx
        if ry < 0:
            ry = -ry

        x = 0
        y = ry
        d1 = (ry * ry) - (rx * rx * ry) + (rx * rx / 4)
        dx = 2 * ry * ry * x
        dy = 2 * rx * rx * y

        while dx < dy:
            Line2D.hline(layer, cx - x, cx + x, cy + y, c, c)
            Line2D.hline(layer, cx - x, cx + x, cy - y, c, c)

            if d1 < 0:
                x += 1
                dx += 2 * ry * ry
                d1 += dx + ry * ry
            else:
                x += 1
                y -= 1
                dx += 2 * ry * ry
                dy -= 2 * rx * rx
                d1 += dx - dy + ry * ry

        d2 = ry * ry * (x + 0.5) * (x + 0.5) + rx * rx * (y - 1) * (y - 1) - rx * rx * ry * ry

        while y >= 0:
            Line2D.hline(layer, cx - x, cx + x, cy + y, c, c)
            Line2D.hline(layer, cx - x, cx + x, cy - y, c, c)

            if d2 > 0:
                y -= 1
                dy -= 2 * rx * rx
                d2 += rx * rx - dy
            else:
                y -= 1
                x += 1
                dx += 2 * ry * ry
                dy -= 2 * rx * rx
                d2 += dx - dy + rx * rx
