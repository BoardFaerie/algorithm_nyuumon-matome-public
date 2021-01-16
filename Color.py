class Color:
    """Color class as numpy array of size (4)(r, g, b, a) used in a layer"""
    # https://ja.wikipedia.org/wiki/ウェブカラー
    # https://ja.wikipedia.org/wiki/アルファチャンネル
    # https://ja.wikipedia.org/wiki/色

    clear_color = np.array([0, 0, 0, 0], dtype='u1')

    white       = np.array([255,    255,    255,    255], dtype='u1')
    lightgray   = np.array([192,    192,    192,    255], dtype='u1')
    gray        = np.array([128,    128,    128,    255], dtype='u1')
    darkgray    = np.array([64,     64,     64,     255], dtype='u1')
    black       = np.array([0,      0,      0,      255], dtype='u1')

    red         = np.array([255,    0,      0,      255], dtype='u1')
    maroon      = np.array([128,    0,      0,      255], dtype='u1')
    yellow      = np.array([255,    255,    0,      255], dtype='u1')
    olive       = np.array([128,    128,    0,      255], dtype='u1')
    lime        = np.array([0,      255,    0,      255], dtype='u1')
    green       = np.array([0,      128,    0,      255], dtype='u1')
    cyan        = np.array([0,      255,    255,    255], dtype='u1')
    teal        = np.array([0,      128,    128,    255], dtype='u1')
    blue        = np.array([0,      0,      255,    255], dtype='u1')
    navy        = np.array([0,      0,      128,    255], dtype='u1')
    magenta     = np.array([255,    0,      255,    255], dtype='u1')
    fuchsia     = np.array([255,    0,      255,    255], dtype='u1')
    purple      = np.array([128,    0,      128,    255], dtype='u1')

    @staticmethod
    def RGB_to_color(r: int, g: int, b: int, a: int=255):
        """Return color from red, green, blue, and alpha, all 0 to 255"""
        return np.clip(np.array([r, g, b, a], dtype='u1'), 0, 255)

    @staticmethod
    def RGB_hex_to_color(text: str, a: int=255):
        """Return color from rgb hex text and alpha (0~255) eg. A040AB, 150"""
        num = int(text, 16)
        r = num // 65536
        g = (num - r * 65536) // 256
        b = num - r * 65536 - g * 256
        return np.clip(np.array([r, g, b, a], dtype='u1'), 0, 255)

    @staticmethod
    def HSV_to_color(h: int, s: int, v: int, a: int=255):
        """Return color from hue (0~360), saturation (0~255), value (0~255), and alpha (0~255)"""
        # https://www.peko-step.com/tool/hsvrgb.html
        h %= 360
        s = np.clip(s, 0, 255)
        v = np.clip(v, 0, 255)
        maxvalue = v
        minvalue = maxvalue - maxvalue * s / 255
        if 0 <= h < 60:
            r = maxvalue
            g = h / 60 * (maxvalue - minvalue) + minvalue
            b = minvalue
        elif 60 <= h < 120:
            r = (120 - h) / 60 * (maxvalue - minvalue) + minvalue
            g = maxvalue
            b = minvalue
        elif 120 <= h < 180:
            r = minvalue
            g = maxvalue
            b = (h - 120) / 60 * (maxvalue - minvalue) + minvalue
        elif 180 <= h < 240:
            r = minvalue
            g = (h - 240) / 60 * (maxvalue - minvalue) + minvalue
            b = maxvalue
        elif 240 <= h < 300:
            r = (h - 240) / 60 * (maxvalue - minvalue) + minvalue
            g = minvalue
            b = maxvalue
        else:
            r = maxvalue
            g = minvalue
            b = (360 - h) / 60 * (maxvalue - minvalue) + minvalue
        r = round(r)
        g = round(g)
        b = round(b)

        return np.clip(np.array([r, g, b, a], dtype='u1'), 0, 255)

    @staticmethod
    def mix(src_color, src_f, dst_color, dst_f):
        """Mix two colors with alpha. Use Canvas.mix for mixing layers. Mainly for internal use. Source is on top of destination."""
        src_a = src_color[:, 3] / 255
        dst_a = dst_color[:, 3] / 255
        out_a = src_a * src_f + dst_a * dst_f
        outafilter = out_a > 0
        out_rgb = np.zeros((src_color.shape[0], 3), dtype='u1')
        out_rgb[outafilter] = np.clip(np.round((src_color[outafilter, 0:3] * np.tile(src_a[outafilter].reshape(-1, 1), (1, 3)) * np.tile(src_f[outafilter].reshape(-1, 1), (1, 3)) + dst_color[outafilter, 0:3] * np.tile(dst_a[outafilter].reshape(-1, 1), (1, 3)) * np.tile(dst_f[outafilter].reshape(-1, 1), (1, 3))) / np.tile(out_a[outafilter].reshape(-1, 1), (1, 3))), 0, 255)
        return np.concatenate([out_rgb, np.clip(np.round(out_a * 255), 0, 255).reshape(-1, 1)], axis=1).astype('u1').copy()

    @staticmethod
    def clear(src_color, dst_color):
        src_f = np.zeros(dst_color.shape[0])
        dst_f = np.zeros(dst_color.shape[0])
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def source(src_color, dst_color):
        src_f = np.ones(dst_color.shape[0])
        dst_f = np.zeros(dst_color.shape[0])
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def destination(src_color, dst_color):
        src_f = np.zeros(dst_color.shape[0])
        dst_f = np.ones(dst_color.shape[0])
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def over(src_color, dst_color):
        src_f = np.ones(dst_color.shape[0])
        dst_f = np.ones(dst_color.shape[0]) - src_color[:, 3] / 255
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def in_(src_color, dst_color):
        src_f = dst_color[:, 3] / 255
        dst_f = np.zeros(dst_color.shape[0])
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def out(src_color, dst_color):
        src_f = np.ones(dst_color.shape[0]) - dst_color[:, 3] / 255
        dst_f = np.zeros(dst_color.shape[0])
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def atop(src_color, dst_color):
        src_f = dst_color[:, 3] / 255
        dst_f = np.ones(dst_color.shape[0]) - src_color[:, 3] / 255
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def xor(src_color, dst_color):
        src_f = np.ones(dst_color.shape[0]) - dst_color[:, 3] / 255
        dst_f = np.ones(dst_color.shape[0]) - src_color[:, 3] / 255
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def add(src_color, dst_color):
        src_f = np.ones(dst_color.shape[0])
        dst_f = np.ones(dst_color.shape[0])
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def weak_add(src_color, dst_color):
        src_f = np.ones(dst_color.shape[0]) * 0.7
        dst_f = np.ones(dst_color.shape[0]) * 0.7
        return Color.mix(src_color, src_f, dst_color, dst_f)

    @staticmethod
    def simple_add(src_color, dst_color):
        return np.clip(src_color + dst_color, 0, 255).astype('u1').copy()
