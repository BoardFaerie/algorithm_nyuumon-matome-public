class Material:
    """Material class for World Objects"""
    # https://yttm-work.jp/model_render/model_render_0001.html
    # https://en.wikipedia.org/wiki/Wavefront_.obj_file
    # http://www.it.hiof.no/~borres/j3d/explain/light/p-materials.html
    # https://www.scratchapixel.com/lessons/3d-basic-rendering/phong-shader-BRDF

    # in order of Ka(RGB ambient, 0~1), Kd(RGB diffuse, 0~1), Ks(RGB specular, 0~1), Ns(specular exponent, 1~1000?), d(alpha, d=1 is opaque, d=0 is transparent)
    ####################         Ka R       G       B    Kd R       G       B    Ks R       G       B       Ns      d
    clear_material      = np.array([0,      0,      0,      0,      0,      0,      0,      0,      0,      1,      0], dtype='f8')

    matte_white         = np.array([0.5,    0.5,    0.5,    1,      1,      1,      0,      0,      0,      1,      1], dtype='f8')
    matte_lightgray     = np.array([0.375,  0.375,  0.375,  0.75,   0.75,   0.75,   0,      0,      0,      1,      1], dtype='f8')
    matte_gray          = np.array([0.25,   0.25,   0.25,   0.5,    0.5,    0.5,    0,      0,      0,      1,      1], dtype='f8')
    matte_darkgray      = np.array([0.125,  0.125,  0.125,  0.25,   0.25,   0.25,   0,      0,      0,      1,      1], dtype='f8')
    matte_black         = np.array([0,      0,      0,      0,      0,      0,      0,      0,      0,      1,      1], dtype='f8')

    matte_red           = np.array([0.5,    0,      0,      1,      0,      0,      0,      0,      0,      1,      1], dtype='f8')
    matte_maroon        = np.array([0.25,   0,      0,      0.5,    0,      0,      0,      0,      0,      1,      1], dtype='f8')
    matte_yellow        = np.array([0.5,    0.5,    0,      1,      1,      0,      0,      0,      0,      1,      1], dtype='f8')
    matte_olive         = np.array([0.25,   0.25,   0,      0.5,    0.5,    0,      0,      0,      0,      1,      1], dtype='f8')
    matte_lime          = np.array([0,      0.5,    0,      0,      1,      0,      0,      0,      0,      1,      1], dtype='f8')
    matte_green         = np.array([0,      0.25,   0,      0,      0.5,    0,      0,      0,      0,      1,      1], dtype='f8')
    matte_cyan          = np.array([0,      0.5,    0.5,    0,      1,      1,      0,      0,      0,      1,      1], dtype='f8')
    matte_teal          = np.array([0,      0.25,   0.25,   0,      0.5,    0.5,    0,      0,      0,      1,      1], dtype='f8')
    matte_blue          = np.array([0,      0,      0.5,    0,      0,      1,      0,      0,      0,      1,      1], dtype='f8')
    matte_navy          = np.array([0,      0,      0.25,   0,      0,      0.5,    0,      0,      0,      1,      1], dtype='f8')
    matte_magenta       = np.array([0.5,    0,      0.5,    1,      0,      1,      0,      0,      0,      1,      1], dtype='f8')
    matte_fuchsia       = np.array([0.5,    0,      0.5,    1,      0,      1,      0,      0,      0,      1,      1], dtype='f8')
    matte_purple        = np.array([0.25,   0,      0.25,   0.5,    0,      0.5,    0,      0,      0,      1,      1], dtype='f8')

    ####################         Ka R       G       B    Kd R       G       B    Ks R       G       B       Ns      d
    brass               = np.array([0.33,   0.22,   0.27,   0.78,   0.57,   0.11,   0.99,   0.94,   0.81,   28,     1], dtype='f8')
    bronze              = np.array([0.21,   0.13,   0.05,   0.71,   0.43,   0.18,   0.39,   0.27,   0.17,   26,     1], dtype='f8')
    polished_bronze     = np.array([0.25,   0.15,   0.06,   0.40,   0.24,   0.10,   0.77,   0.46,   0.20,   77,     1], dtype='f8')
    chrome              = np.array([0.25,   0.25,   0.25,   0.40,   0.40,   0.40,   0.78,   0.78,   0.78,   77,     1], dtype='f8')
    copper              = np.array([0.19,   0.07,   0.02,   0.70,   0.27,   0.08,   0.26,   0.14,   0.09,   13,     1], dtype='f8')
    polished_copper     = np.array([0.23,   0.09,   0.03,   0.55,   0.21,   0.07,   0.58,   0.22,   0.70,   51,     1], dtype='f8')
    gold                = np.array([0.25,   0.20,   0.07,   0.75,   0.61,   0.23,   0.63,   0.56,   0.37,   51,     1], dtype='f8')
    polished_gold       = np.array([0.25,   0.22,   0.06,   0.35,   0.31,   0.09,   0.80,   0.72,   0.21,   83,     1], dtype='f8')
    tin                 = np.array([0.11,   0.06,   0.11,   0.43,   0.47,   0.54,   0.33,   0.33,   0.52,   10,     1], dtype='f8')
    silver              = np.array([0.19,   0.19,   0.19,   0.51,   0.51,   0.51,   0.51,   0.51,   0.51,   51,     1], dtype='f8')
    polished_silver     = np.array([0.23,   0.23,   0.23,   0.28,   0.28,   0.28,   0.77,   0.77,   0.77,   90,     1], dtype='f8')
    emerald             = np.array([0.02,   0.17,   0.02,   0.08,   0.61,   0.08,   0.63,   0.73,   0.63,   77,     1], dtype='f8')
    jade                = np.array([0.14,   0.22,   0.16,   0.54,   0.89,   0.63,   0.32,   0.32,   0.32,   13,     1], dtype='f8')
    obsidian            = np.array([0.05,   0.05,   0.06,   0.18,   0.17,   0.23,   0.33,   0.33,   0.35,   38,     1], dtype='f8')
    perl                = np.array([0.25,   0.21,   0.21,   1.00,   0.83,   0.83,   0.30,   0.30,   0.30,   11,     1], dtype='f8')
    ruby                = np.array([0.17,   0.01,   0.01,   0.61,   0.04,   0.04,   0.73,   0.63,   0.63,   77,     1], dtype='f8')
    turquoise           = np.array([0.10,   0.19,   0.17,   0.01,   0.01,   0.01,   0.50,   0.50,   0.50,   32,     1], dtype='f8')

    ####################         Ka R       G       B    Kd R       G       B    Ks R       G       B       Ns      d
    plastic_white       = np.array([0.10,   0.10,   0.10,   0.50,   0.50,   0.50,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_lightgray   = np.array([0.08,   0.08,   0.08,   0.38,   0.38,   0.38,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_gray        = np.array([0.05,   0.05,   0.05,   0.25,   0.25,   0.25,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_darkgray    = np.array([0.03,   0.03,   0.03,   0.13,   0.13,   0.13,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_black       = np.array([0.01,   0.01,   0.01,   0.01,   0.01,   0.01,   0.50,   0.50,   0.50,   32,     1], dtype='f8')

    plastic_red         = np.array([0.10,   0.01,   0.01,   0.50,   0.01,   0.01,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_maroon      = np.array([0.05,   0.01,   0.01,   0.25,   0.01,   0.01,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_yellow      = np.array([0.10,   0.10,   0.01,   0.50,   0.50,   0.01,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_olive       = np.array([0.05,   0.05,   0.01,   0.25,   0.25,   0.01,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_lime        = np.array([0.01,   0.10,   0.01,   0.01,   0.50,   0.01,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_green       = np.array([0.01,   0.05,   0.01,   0.01,   0.25,   0.01,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_cyan        = np.array([0.01,   0.10,   0.10,   0.01,   0.50,   0.50,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_teal        = np.array([0.01,   0.05,   0.05,   0.01,   0.25,   0.25,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_blue        = np.array([0.01,   0.01,   0.10,   0.01,   0.01,   0.50,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_navy        = np.array([0.01,   0.01,   0.05,   0.01,   0.01,   0.25,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_magenta     = np.array([0.10,   0.01,   0.10,   0.50,   0.01,   0.50,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_fuchsia     = np.array([0.10,   0.01,   0.10,   0.50,   0.01,   0.50,   0.50,   0.50,   0.50,   32,     1], dtype='f8')
    plastic_purple      = np.array([0.05,   0.01,   0.05,   0.25,   0.01,   0.25,   0.50,   0.50,   0.50,   32,     1], dtype='f8')

    ####################         Ka R       G       B    Kd R       G       B    Ks R       G       B       Ns      d
    rubber_white        = np.array([0.05,   0.05,   0.05,   0.50,   0.50,   0.50,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_lightgray    = np.array([0.04,   0.04,   0.04,   0.38,   0.38,   0.38,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_gray         = np.array([0.03,   0.03,   0.03,   0.25,   0.25,   0.25,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_darkgray     = np.array([0.02,   0.02,   0.02,   0.13,   0.13,   0.13,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_black        = np.array([0.01,   0.01,   0.01,   0.01,   0.01,   0.01,   0.10,   0.10,   0.10,   10,     1], dtype='f8')

    rubber_red          = np.array([0.05,   0.01,   0.01,   0.50,   0.30,   0.30,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_maroon       = np.array([0.03,   0.01,   0.01,   0.40,   0.30,   0.30,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_yellow       = np.array([0.05,   0.05,   0.01,   0.50,   0.50,   0.30,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_olive        = np.array([0.03,   0.03,   0.01,   0.40,   0.40,   0.30,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_lime         = np.array([0.01,   0.05,   0.01,   0.30,   0.50,   0.30,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_green        = np.array([0.01,   0.03,   0.01,   0.30,   0.40,   0.30,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_cyan         = np.array([0.01,   0.05,   0.05,   0.30,   0.50,   0.50,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_teal         = np.array([0.01,   0.03,   0.03,   0.30,   0.40,   0.40,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_blue         = np.array([0.01,   0.01,   0.05,   0.30,   0.30,   0.50,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_navy         = np.array([0.01,   0.01,   0.03,   0.30,   0.30,   0.40,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_magenta      = np.array([0.05,   0.01,   0.05,   0.50,   0.30,   0.50,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_fuchsia      = np.array([0.05,   0.01,   0.05,   0.50,   0.30,   0.50,   0.10,   0.10,   0.10,   10,     1], dtype='f8')
    rubber_purple       = np.array([0.03,   0.01,   0.03,   0.40,   0.30,   0.40,   0.10,   0.10,   0.10,   10,     1], dtype='f8')

    @staticmethod
    def color_to_matte_material(color):
        return np.concatenate([color[0:3].copy() / 255 / 2, color[0:3].copy() / 255, np.zeros(3), np.array([1]), np.array([color[3].copy() / 255])], axis=0).astype("f8")

    @staticmethod
    def color_to_plastic_material(color):
        return np.concatenate([np.zeros(3), color[0:3].copy() / 255 / 2 + 0.01, color[0:3].copy() / 255 / 5 + 0.5, np.array([32]), np.array([color[3].copy() / 255])], axis=0).astype("f8")

    @staticmethod
    def color_to_rubber_material(color):
        return np.concatenate([color[0:3].copy() / 255 / 20, color[0:3].copy() / 255 / 2 + 0.01, color[0:3].copy() / 255 * 0.7 + 0.01, np.array([10]), np.array([color[3].copy() / 255])], axis=0).astype("f8")
