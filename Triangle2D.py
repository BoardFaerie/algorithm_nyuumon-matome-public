class Triangle2D:
    """Triangle class for a layer"""

    @staticmethod
    def triangle(layer:Layer, x0:int, y0:int, x1:int, y1:int, x2:int, y2:int, c0=None, c1=None, c2=None, z0=0, z1=0, z2=0, n0=None, n1=None, n2=None, lights=None, shadows=None, antialias=False):
        """Draw a triangle with vertex (x0, y0), (x1, y1), (x2, y2) and color c"""
        Line2D.line(layer, x0, y0, x1, y1, c0, c1, z0, z1, n0, n1, lights, shadows, antialias, True)
        Line2D.line(layer, x1, y1, x2, y2, c1, c2, z1, z2, n1, n2, lights, shadows, antialias, True)
        Line2D.line(layer, x2, y2, x0, y0, c2, c0, z2, z0, n2, n0, lights, shadows, antialias, True)

    @staticmethod
    def filled_flat_triangle(layer:Layer, x0:int, y0:int, x1:int, y1:int, x2:int, y2:int, c0=None, c1=None, c2=None, z0=0, z1=0, z2=0, n0=None, n1=None, n2=None, lights=None, shadows=None, antialias=False):
        #print("filled_flat_triangle: x0: ", x0, ", y0: ", y0, ", x1: ", x1, ", y1: ", y1, ", x2: ", x2, ", y2: ", y2, ", c0: ", c0, ", c1: ", c1, ", c2: ", c2, ", z0: ", z0, ", z1: ", z1, ", z2: ", z2, ", n0: ", n0, ", n1: ", n1, ", n2: ", n2, ", lights: ", lights, ", shadows: ", shadows)

        dx1 = abs(x1 - x0)
        dx2 = abs(x2 - x0)
        dy = abs(y1 - y0)

        sx1 = 1 if x0 < x1 else -1
        sx2 = 1 if x0 < x2 else -1
        sy = 1 if y0 < y1 else -1

        err1 = dx1 - dy
        err2 = dx2 - dy

        xnow1 = x0
        xnow2 = x0
        ynow = y0
        finish = False

        if n0 is not None:
            xarr = []
            yarr = []
            carr = []
            zarr = []
            narr = []
            while True:
                while True:
                    #layer.draw_point(xnow1, ynow, c0 + (c1 - c0) * (ynow - y0) / (y1 - y0), z0 + (z1 - z0) * (ynow - y0) / (y1 - y0), n0 + (n1 - n0) * (ynow - y0) / (y1 - y0), lights, shadows)
                    if xnow1 == x1 and ynow == y1:
                        finish = True
                        break
                    e21 = 2 * err1
                    if e21 > -dy:
                        err1 -= dy
                        xnow1 += sx1
                    if e21 < dx1:
                        break

                while True:
                    #layer.draw_point(xnow2, ynow, c0 + (c2 - c0) * (ynow - y0) / (y2 - y0), z0 + (z2 - z0) * (ynow - y0) / (y2 - y0), n0 + (n2 - n0) * (ynow - y0) / (y2 - y0), lights, shadows)
                    if xnow2 == x2 and ynow == y2:
                        finish = True
                        break
                    e22 = 2 * err2
                    if e22 > -dy:
                        err2 -= dy
                        xnow2 += sx2
                    if e22 < dx2:
                        break
                xret, yret, cret, zret, nret = Line2D.hline_triangle(layer, xnow1, xnow2, ynow, c0 + (c1 - c0) * (ynow - y0) / (y1 - y0), c0 + (c2 - c0) * (ynow - y0) / (y2 - y0), z0 + (z1 - z0) * (ynow - y0) / (y1 - y0), z0 + (z2 - z0) * (ynow - y0) / (y2 - y0), n0 + (n1 - n0) * (ynow - y0) / (y1 - y0), n0 + (n2 - n0) * (ynow - y0) / (y2 - y0))
                if xret is not None:
                    xarr.append(xret)
                    yarr.append(yret)
                    carr.append(cret)
                    zarr.append(zret)
                    narr.append(nret)
                if ((xnow1 == x1 or xnow2 == x2) and ynow == y2) or finish:
                    break
                err1 += dx1
                err2 += dx2
                ynow += sy
            if len(xarr) > 0:
                layer.draw(np.concatenate(xarr, axis=0), np.concatenate(yarr, axis=0), np.concatenate(carr, axis=0), np.concatenate(zarr, axis=0), np.concatenate(narr, axis=0), lights, shadows)
        else:
            xarr = []
            yarr = []
            zarr = []
            while True:
                while True:
                    #layer.draw_point(xnow1, ynow, z=z0 + (z1 - z0) * (ynow - y0) / (y1 - y0))
                    if xnow1 == x1 and ynow == y1:
                        finish = True
                        break
                    e21 = 2 * err1
                    if e21 > -dy:
                        err1 -= dy
                        xnow1 += sx1
                    if e21 < dx1:
                        break

                while True:
                    #layer.draw_point(xnow2, ynow, z=z0 + (z2 - z0) * (ynow - y0) / (y2 - y0))
                    if xnow2 == x2 and ynow == y2:
                        finish = True
                        break
                    e22 = 2 * err2
                    if e22 > -dy:
                        err2 -= dy
                        xnow2 += sx2
                    if e22 < dx2:
                        break
                xret, yret, zret = Line2D.hline_triangle_shadow(layer, xnow1, xnow2, ynow, z0 + (z1 - z0) * (ynow - y0) / (y1 - y0), z1=z0 + (z2 - z0) * (ynow - y0) / (y2 - y0))
                if xret is not None:
                    xarr.append(xret)
                    yarr.append(yret)
                    zarr.append(zret)
                if ((xnow1 == x1 or xnow2 == x2) and ynow == y2) or finish:
                    break
                err1 += dx1
                err2 += dx2
                ynow += sy
            if len(xarr) > 0:
                layer.draw(np.concatenate(xarr, axis=0), np.concatenate(yarr, axis=0), z=np.concatenate(zarr, axis=0))

    @staticmethod
    def filled_triangle(layer:Layer, x0:int, y0:int, x1:int, y1:int, x2:int, y2:int, c0=None, c1=None, c2=None, z0=0, z1=0, z2=0, n0=None, n1=None, n2=None, lights=None, shadows=None, antialias=False):
        """Draw a filled triangle with vertex (x0, y0), (x1, y1), (x2, y2) and color c"""
        # Bresenham
        # http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html

        #print("filled_triangle: x0: ", x0, ", y0: ", y0, ", x1: ", x1, ", y1: ", y1, ", x2: ", x2, ", y2: ", y2, ", c0: ", c0, ", c1: ", c1, ", c2: ", c2, ", z0: ", z0, ", z1: ", z1, ", z2: ", z2, ", n0: ", n0, ", n1: ", n1, ", n2: ", n2, ", lights: ", lights, ", shadows: ", shadows)

        if y0 == y1 == y2:
            Line2D.hline(layer, x0, x1, y0, c0, c1, z0, z1, n0, n1, lights, shadows)
            Line2D.hline(layer, x1, x2, y0, c1, c2, z1, z2, n1, n2, lights, shadows)
            return
    
        if y1 < y0:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            z0, z1 = z1, z0
            if n0 is not None:
                c0, c1 = c1.copy(), c0.copy()
                n0, n1 = n1.copy(), n0.copy()
        if y2 < y0:
            x0, x2 = x2, x0
            y0, y2 = y2, y0
            z0, z2 = z2, z0
            if n0 is not None:
                c0, c2 = c2.copy(), c0.copy()
                n0, n2 = n2.copy(), n0.copy()
        if y2 < y1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            z1, z2 = z2, z1
            if n0 is not None:
                c1, c2 = c2.copy(), c1.copy()
                n1, n2 = n2.copy(), n1.copy()
        
        if y1 == y2:
            Line2D.hline(layer, x1, x2, y1, c1, c2, z1, z2, n1, n2, lights, shadows)
            Triangle2D.filled_flat_triangle(layer, x0, y0, x1, y1, x2, y2, c0, c1, c2, z0, z1, z2, n0, n1, n2, lights, shadows, antialias)
        elif y0 == y1:
            Line2D.hline(layer, x0, x1, y0, c0, c1, z0, z1, n0, n1, lights, shadows)
            Triangle2D.filled_flat_triangle(layer, x2, y2, x0, y0, x1, y1, c2, c0, c1, z2, z0, z1, n2, n0, n1, lights, shadows, antialias)
        else:
            x3 = x0 + round((x2 - x0) * (y1 - y0) / (y2 - y0))
            y3 = y1
            z3 = z0 + (z2 - z0) * (y1 - y0) / (y2 - y0)
            if n0 is not None:
                c3 = c0 + (c2 - c0) * (y1 - y0) / (y2 - y0)
                n3 = n0 + (n2 - n0) * (y1 - y0) / (y2 - y0)
                Line2D.hline(layer, x1, x3, y1, c1, c3, z1, z3, n1, n3, lights, shadows)
                Triangle2D.filled_flat_triangle(layer, x0, y0, x1, y1, x3, y3, c0, c1, c3, z0, z1, z3, n0, n1, n3, lights, shadows, antialias)
                Triangle2D.filled_flat_triangle(layer, x2, y2, x1, y1, x3, y3, c2, c1, c3, z2, z1, z3, n2, n1, n3, lights, shadows, antialias)
            else:
                Line2D.hline(layer, x1, x3, y1, z0=z1, z1=z3)
                Triangle2D.filled_flat_triangle(layer, x0, y0, x1, y1, x3, y3, z0=z0, z1=z1, z2=z3, antialias=antialias)
                Triangle2D.filled_flat_triangle(layer, x2, y2, x1, y1, x3, y3, z0=z2, z1=z1, z2=z3, antialias=antialias)
