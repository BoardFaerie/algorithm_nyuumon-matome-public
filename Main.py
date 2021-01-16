# https://www.ngdc.noaa.gov/mgg/image/images/etopo2icosahedron.pdf
# https://solarviews.com/cap/ico/icoearth.htm
# https://ja.wikipedia.org/wiki/軌道要素
# https://ja.wikipedia.org/wiki/太陽
# https://ja.wikipedia.org/wiki/地球
# https://ja.wikipedia.org/wiki/月
# https://ja.wikipedia.org/wiki/ケプラーの方程式
# https://en.wikipedia.org/wiki/Kepler's_equation
# http://fnorio.com/0158Kepler_equation/Kepler_equation.html

with warnings.catch_warnings():
    warnings.simplefilter("error")

    print("Initializing...")

    world = World()
    canvas = Canvas(Settings.WIDTH, Settings.HEIGHT)
    cam = Camera(pos=np.array([0, 0, -30,]))

    imgs = []
    shadows_list = []
    fig, ax = plt.subplots()

    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    ax.axis('off')
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)


    # Materials
    M = Material()
    wh = M.plastic_white
    lg = M.plastic_lightgray
    ye = M.rubber_yellow
    ol = M.rubber_olive
    gr = M.rubber_green
    cy = M.plastic_cyan
    bl = M.plastic_blue
    bw = M.color_to_rubber_material(Color.RGB_to_color(153, 76, 0))

    sun_material = np.tile(np.array([1000,    1000,    0,      0,      0,      0,      0,      0,      0,      1,      1], dtype='f8').reshape(1, -1), (80, 1))
    earth_material = np.stack([
    # 0 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        cy, cy, cy, cy, wh, wh, wh, bl, wh, wh, wh, wh, wh, wh, wh, wh,     wh, wh, bl, wh, bl, wh, bl, wh, bl, bl, wh, bl, bl, wh, wh, bl,     wh, wh, wh, bl, bl, bl, wh, bl, wh, wh, bl, bl, bl, bl, bl, bl,     bl, bl, wh, bl, wh, wh, wh, wh, wh, bl, wh, bl, wh, wh, wh, wh,
        wh, wh, wh, gr, gr, gr, bl, gr, bl, bl, wh, bl, gr, gr, gr, gr,     gr, gr, gr, gr, gr, gr, gr, wh, wh, wh, wh, wh, gr, gr, gr, bl,     bl, wh, bl, wh, wh, bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, bl,     bl, gr, gr, gr, gr, gr, gr, bl, gr, gr, gr, bl, gr, gr, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, gr, bl, gr,     gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        gr, gr, gr, gr, gr, gr, bl, gr, gr, gr, bl, gr, gr, gr, gr, gr,     ol, ol, gr, gr, gr, gr, gr, gr, gr, gr, bl, gr, gr, gr, gr, gr,     gr, gr, gr, gr, gr, ol, gr, gr, gr, bl, bl, bl, gr, gr, gr, gr,     ol, ol, ol, ol, ol, gr, gr, gr, gr, gr, gr, gr, ol, ol, ol, ol,
    # 1 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        cy, cy, cy, cy, wh, bl, cy, bl, wh, wh, bl, bl, wh, wh, bl, wh,     wh, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, wh, gr, wh, wh, bl, gr, bl, gr, gr, gr, bl, wh, wh, gr, wh,     wh, wh, bl, wh, bl, wh, wh, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, gr, bl, bl, bl, bl, bl,     bl, bl, bl, bl, gr, bl, gr, bl, gr, bl, bl, bl, gr, gr, gr, wh,     bl, bl, gr, gr, gr, bl, gr, gr, bl, gr, gr, gr, gr, gr, gr, gr,     bl, gr, bl, ol, gr, ol, gr, bl, gr, gr, gr, bl, bl, ol, gr, ol,
        gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr,     bl, bl, gr, gr, bl, gr, gr, bl, gr, gr, bl, gr, bl, bl, bl, bl,     bl, ol, ol, gr, bl, bl, gr, bl, bl, bl, bl, bl, bl, ye, ye, bl,     gr, bl, bl, bl, gr, ol, bl, ye, bl, ye, ye, ye, ol, ye, ye, ye,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, gr, bl, bl, bl, bl, bl, gr, ol, ye, gr, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
    # 2 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        cy, cy, cy, cy, bl, bl, bl, bl, wh, bl, wh, bl, bl, bl, wh, bl,     bl, wh, bl, bl, wh, wh, wh, wh, bl, wh, wh, wh, wh, gr, wh, gr,     wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, gr, wh, wh, gr, gr, gr,     bl, bl, bl, bl, bl, gr, wh, gr, wh, gr, gr, gr, bl, gr, gr, gr,
        gr, wh, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr,     ol, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, ye, gr, gr, gr,     gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, wh, wh, gr,     ye, gr, ye, gr, wh, gr, gr, wh, gr, gr, gr, ye, gr, wh, wh, gr,
        gr, gr, gr, wh, gr, gr, gr, ye, gr, gr, ye, ye, ye, ye, ye, ye,     gr, bw, bw, ye, ye, ye, bw, ye, bw, bw, ye, ye, wh, wh, ye, ol,     bw, ye, ye, ye, ye, ol, bw, ol, gr, gr, gr, gr, ye, wh, ol, ol,     gr, ye, ye, ye, wh, wh, wh, bw, wh, ol, bw, bw, wh, wh, wh, ol,
        gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, bl, gr, gr, gr, bl,     gr, wh, gr, gr, gr, bl, bl, bl, bl, ye, ye, ye, ol, ye, ye, bw,     bw, ol, bw, bw, ol, gr, gr, ye, wh, ol, ol, ye, ye, ye, bw, ye,     bl, bw, gr, ol, ye, ye, gr, ye, gr, ol, ol, ye, ye, ye, ye, ye,
    # 3 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        cy, cy, cy, cy, cy, cy, cy, wh, cy, wh, wh, wh, cy, wh, wh, bl,     bl, bl, bl, wh, wh, wh, bl, wh, bl, bl, wh, wh, wh, wh, wh, wh,     wh, bl, bl, wh, wh, wh, wh, wh, wh, wh, bl, wh, wh, wh, bl, wh,     wh, wh, wh, wh, wh, wh, wh, gr, wh, gr, wh, gr, wh, gr, wh, gr,
        wh, wh, wh, gr, ol, ol, wh, wh, gr, wh, wh, bl, ol, gr, wh, gr,     ol, wh, wh, bl, gr, gr, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, wh, wh, bl, bl, bl, bl, bl, bl, bl, bl, bl,     gr, bl, bl, bl, gr, bl, gr, bl, bl, bl, bl, bl, gr, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        wh, wh, wh, gr, gr, ol, gr, ol, gr, bw, ol, gr, gr, ye, ye, ye,     ye, ol, ol, gr, bl, bl, ol, gr, bw, gr, gr, gr, gr, bl, gr, bl,     gr, bl, bl, bl, bl, gr, gr, bl, gr, bl, bl, bl, bl, gr, bl, bl,     ye, ye, ol, ye, gr, gr, gr, gr, gr, gr, bl, gr, gr, ol, gr, gr,
    # 4 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        cy, cy, cy, cy, cy, cy, cy, wh, cy, bl, wh, cy, cy, wh, wh, wh,     bl, bl, bl, wh, wh, wh, bl, wh, bl, bl, wh, bl, wh, wh, wh, wh,     wh, bl, wh, wh, wh, wh, wh, wh, wh, wh, wh, gr, wh, gr, wh, wh,     bl, bl, wh, bl, wh, bl, wh, bl, wh, gr, wh, wh, bl, bl, bl, bl,
        bl, bl, bl, bl, gr, gr, bl, bl, gr, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, wh, bl, bl, wh, wh, gr, gr, gr, gr, gr, bl, bl, gr, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        gr, gr, gr, gr, bw, bw, gr, gr, ol, ol, gr, gr, wh, bl, gr, bl,     bl, bl, gr, bl, bl, gr, gr, gr, gr, gr, gr, bw, bl, bl, gr, bl,     gr, bw, bw, bw, bw, bw, bw, bw, gr, bw, ol, bw, gr, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
    # 5 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        gr, gr, gr, bl, bl, bl, bl, bl, gr, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
    # 6 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bw, bw, gr, gr, bw, gr, gr, bl, gr, bl, bl, bl, ol, gr, bl, gr,     gr, gr, bl, gr, gr, gr, bl, gr, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, gr, bl, bl, bl, gr, bl, bl, bl, bl, bl, gr, bl, gr, bl,     bl, bl, bl, bl, bl, bl, bl, bl, gr, gr, gr, gr, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, gr, gr, gr, gr, gr,     gr, gr, gr, gr, gr, gr, bl, gr, bl, bl, bl, bl, gr, bl, bl, bl,     bl, gr, gr, bl, gr, bl, bl, bl, bl, bl, bl, bl, bl, gr, bl, bl,     gr, gr, gr, ol, gr, gr, gr, gr, bw, bw, bl, gr, gr, gr, gr, gr,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, gr, bl, gr,
        bl, bl, bl, bl, bl, gr, bl, gr, bw, gr, gr, gr, bl, bl, gr, bl,     bl, bw, bw, bw, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr,     gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr,     bl, bl, bw, bl, bl, bl, bw, bw, bw, bw, gr, bw, bl, bl, bw, bl,
    # 7 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, gr,
        gr, gr, gr, gr, gr, gr, gr, gr, bl, bl, bl, gr, gr, gr, gr, gr,     gr, gr, gr, bl, bl, gr, gr, bl, gr, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     gr, gr, bl, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr,     gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr,     gr, gr, gr, gr, gr, bl, bl, bl, bl, bl, bl, bl, gr, gr, bl, gr,     gr, gr, gr, bw, bw, gr, gr, gr, gr, gr, gr, gr, bw, bw, gr, bw,
    # 8 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, ye, bl, bl, bl, ye, ye, ye, ye, ye,     bl, bl, bl, ye, ye, ye, ye, ye, bw, ye, ye, ye, ye, ye, ye, ye,     bl, bl, bl, bl, bl, bl, bl, bl, ye, bw, bw, gr, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, gr, gr, gr, gr, gr, bw, gr, bl, bl, gr, bl,     bl, bl, gr, bl, gr, gr, gr, ye, gr, bw, bw, ye, bw, ye, ye, ye,     ye, ye, ye, ye, ye, ye, ye, ye, ye, ye, ye, ye, ye, ye, ye, ye,     bl, bl, bl, bl, bl, gr, gr, gr, gr, bw, ye, bw, gr, gr, gr, gr,
        ye, ye, ye, bw, bw, bw, ye, bw, ye, ye, ye, ye, ye, ye, ye, bw,     ye, ye, ye, ye, ye, bw, ye, bw, ye, ye, bw, ye, ye, ye, ye, ye,     ye, ye, ye, ye, ye, ye, ye, ye, ye, ol, ye, ye, ye, ye, ye, ye,     ye, bl, ye, ol, ol, bw, ye, bw, ye, ye, ye, bw, gr, gr, gr, gr,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, gr, gr, gr, gr, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
    # 9 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bl, bl, bl, ol, ol, bw, bl, bw, bl, bl, bl, bw, ol, ol, ol, ye,     ye, ol, bw, bw, bw, gr, bw, gr, bw, bw, bl, bw, gr, gr, gr, bw,     bw, bw, ye, gr, ye, ye, ol, gr, bl, bl, bl, bl, gr, gr, ol, bw,     ye, bw, bw, bw, gr, gr, gr, gr, bw, gr, gr, gr, gr, gr, gr, gr,
        gr, gr, gr, gr, gr, gr, gr, bl, gr, gr, bl, gr, gr, gr, gr, gr,     gr, gr, gr, bl, gr, gr, gr, gr, gr, gr, gr, gr, gr, bl, bl, bl,     gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     gr, gr, gr, ol, gr, bl, gr, bl, gr, bl, bl, bl, gr, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     gr, gr, bl, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     gr, gr, gr, bl, bl, gr, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, gr, bl, bl, gr, bl,     bl, bw, gr, bw, bw, ol, gr, ol, gr, gr, gr, ol, ye, bw, ol, bw,     gr, gr, ol, ol, ol, ol, gr, ol, gr, gr, bl, gr, ol, ol, gr, bw,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
    #10 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        ye, ye, ye, bw, bw, ye, ye, ye, ye, bl, ol, ye, bw, bw, ye, bw,     bw, ye, ye, ye, ye, ye, ye, ye, ye, bl, ol, bw, bl, bl, ye, bl,     bw, bw, bw, bl, bl, bl, bw, bl, bw, bw, ol, ol, bl, bl, bl, bl,     bw, bl, bl, ye, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, gr, gr, gr, ol,     bl, bl, bl, bl, bl, bl, bw, bw, ye, ye, ye, ol, gr, gr, bw, ol,     bl, bl, bl, bl, bl, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        ye, ye, ol, ol, ol, bw, ol, bw, wh, wh, wh, bw, bw, gr, bw, ol,     bl, bl, gr, bl, bl, bl, gr, gr, gr, ol, wh, gr, bl, gr, gr, bl,     wh, gr, wh, gr, gr, gr, wh, ol, ol, ol, ol, ol, gr, gr, gr, gr,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
    #11 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        gr, gr, bw, gr, gr, bl, bw, bl, bl, gr, bl, bl, gr, ol, gr, ol,     ol, ol, gr, bl, gr, gr, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, gr, bl, gr, bl, bl, gr, bl, bl, gr, gr, gr,     gr, gr, bl, bl, bl, bl, gr, gr, gr, gr, bl, gr, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, gr, gr, bl, gr, bl, bl, bl, bl,     bl, bl, bl, bl, bl, gr, gr, gr, gr, bl, bl, bl, bl, bl, gr, bl,     gr, gr, gr, bl, bl, bl, bl, bl, bl, gr, bl, gr, gr, gr, gr, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, gr, gr, bl, bl, bl, bl, gr, bl, gr, bl, bl, bl,     bl, bl, bl, ye, ye, ol, gr, ye, gr, ye, gr, ye, bw, bw, ol, gr,     gr, ol, ol, ol, ye, ye, ol, ye, ye, ye, ye, ye, ye, gr, ye, gr,     bl, bl, ye, bl, ol, ye, gr, ol, ye, gr, ol, gr, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
    #12 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        gr, ol, gr, ol, ol, ol, ol, bl, gr, bl, bl, bl, bl, bl, bl, bl,     bl, gr, bl, bl, bl, bl, bl, bl, gr, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, gr, gr, bl, gr, bl, gr, bl, bl, bl, bl, bl, gr, bl, bl, bl,
        gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, gr, gr, bl, gr, bl, bl, bl, gr, bl, gr, bl, bl, bl, gr,     bl, bl, bl, gr, bl, bl, gr, gr, gr, gr, bl, gr, bl, bl, gr, bl,     bl, bl, bl, bl, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, gr, ol, ye, gr, gr, gr, bl, bl, bl, bl, ye, ol, gr, ol,
    #13 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, gr, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, gr, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, gr, gr, bl, gr, bl, bl, bl, bl, gr, ol, ol, ol,
    #14 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, bl, bl, bl, bl, gr, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
    #15 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, wh, wh, wh, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, wh, wh, bl, wh,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh,
    #16 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bw, bw, gr, bw, bw, gr, gr, gr, gr, gr, gr, gr, bw, bw, gr, bw,     bw, bl, gr, bl, bl, bl, gr, bl, gr, bl, gr, bl, bl, bl, bl, bl,     gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     wh, wh, bl, wh, wh, bl, bl, gr, bl, bl, bl, bl, wh, wh, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, wh, wh, bl, bl, bl, bl, bl, bl, wh, wh, bl, wh,     wh, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, wh,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, wh,     wh, wh, bl, wh, bl, bl, bl, wh, bl, wh, wh, wh, wh, wh, wh, wh,
    #17 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bw, bw, gr, bl, bl, bl, gr, bl, gr, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, wh,     wh, wh, bl, wh, wh, bl, bl, wh, bl, bl, bl, bl, wh, wh, wh, wh,     bl, bl, bl, bl, wh, bl, bl, bl, bl, bl, bl, bl, wh, wh, wh, wh,     wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh,
    #18 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, gr, gr, bl, gr, gr, gr, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, ol, bl, bl, bl, bl, bl,     ol, bl, gr, bl, bl, gr, gr, gr, bw, bw, ol, bw, bl, bl, gr, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, wh, wh, wh,     wh, wh, wh, wh, wh, wh, wh, wh, bl, bl, bl, bl, wh, wh, wh, wh,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, wh, wh, wh, wh,     wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh, wh,
    #19 0               4               8               12                  16              20              24              28                  32              36              40              44                  48              52              56              60
        ol, gr, gr, gr, gr, gr, gr, bl, bl, bl, bl, bl, gr, bl, bl, gr,     gr, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, gr, bl, bl, bl, bl,     gr, gr, bl, bl, bl, bl, gr, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,
        bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, wh, wh, bl, wh,     wh, wh, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl, bl,     wh, wh, bl, wh, wh, bl, bl, bl, bl, wh, bl, bl, wh, wh, bl, wh,
        ])
    sun_material = np.tile(np.array([1000,    1000,    0,      0,      0,      0,      0,      0,      0,      1,      1], dtype='f8').reshape(1, -1), (80, 1))
    moon_material = np.tile(np.array([0.10,   0.10,   0.14,   0.38,   0.38,   0.38,   0.65,   0.65,   0.65,   10,     1], dtype='f8').reshape(1, -1), (80, 1))

    # Objects
    # size
    #  units           km
    #     10     =      6378    (Earth equator radius)
    #      1     =       637.8
    #      9.966 =      6356    (Earth polar radius)
    #   1091     =    696000    (Sun equator radius)
    #      5.450 =      3475.8  (Moon equator radius)
    #      5.443 =      3471.3  (Moon polar radius)
    # 230636     = 147100000    (Earth periapsis radius) → 23063.6
    # 238476     = 152100000    (Earth apoapsis radius) → 23847.6
    #  569.6     =    363304    (Moon periapsis radius) → 56.96
    #  635.8     =    405495    (Moon apoapsis radius) → 63.58

    # ccentricity
    # Earth         0.0167
    # Moon          0.0549

    Sun = WorldObject.sphere3D(pos=np.array([0, 0, 23847.6]), size=np.array([1091, 1091, 1091]), material=sun_material, enable_shadow=False)
    Earth_base = WorldObject.sphere3D(pos=np.array([0, 0, 0]), size=np.array([10, 9.966, 10]), rot=Quaternion.euler_to_quaternion(0, 0, np.pi * 23.4 / 180), material=earth_material, div=4)
    Moon = WorldObject.sphere3D(pos=np.array([0, 0, -60]), size=np.array([5.450, 5.443, 5.450]), material=moon_material)

    # Lights
    ambientlight = Light(light_type=0, intensity=1)
    directionallight = Light(pos=np.array([0, 0, 23847.6]), rot=Quaternion.euler_to_quaternion(0, 0, 0), light_type=2, intensity=3, intensity2=3)
    #pointlight1 = Light(pos=np.array([0, 0, 23847.6]), rot=Quaternion.euler_to_quaternion(0, 0, 0), light_type=1, intensity=3, intensity2=3)
    #pointlight2 = Light(pos=np.array([0, 0, 23847.6]), rot=Quaternion.euler_to_quaternion(0, np.pi / 2, 0), light_type=1, intensity=3, intensity2=3)
    #pointlight3 = Light(pos=np.array([0, 0, 23847.6]), rot=Quaternion.euler_to_quaternion(0, np.pi, 0), light_type=1, intensity=3, intensity2=3)
    #pointlight4 = Light(pos=np.array([0, 0, 23847.6]), rot=Quaternion.euler_to_quaternion(0, -np.pi / 2, 0), light_type=1, intensity=3, intensity2=3)
    #pointlight5 = Light(pos=np.array([0, 0, 23847.6]), rot=Quaternion.euler_to_quaternion(0, 0, np.pi / 2), light_type=1, intensity=3, intensity2=3)
    #pointlight6 = Light(pos=np.array([0, 0, 23847.6]), rot=Quaternion.euler_to_quaternion(0, 0, -np.pi / 2), light_type=1, intensity=3, intensity2=3)



    max_time = 64 # 64


    # instantiation
    def instantiate(obj):
        if isinstance(obj, WorldObject):
            world.objects.append(obj)
        elif isinstance(obj, Light):
            world.lights.append(obj)

    # Lights
    instantiate(ambientlight)
    instantiate(directionallight)
    #instantiate(pointlight1)
    #instantiate(pointlight2)
    #instantiate(pointlight3)
    #instantiate(pointlight4)
    #instantiate(pointlight5)
    #instantiate(pointlight6)

    # Objects
    instantiate(Sun)
    instantiate(Earth_base)
    instantiate(Moon)


    moon_c = np.cos(np.pi * 5.1 / 180)
    moon_s = np.sin(np.pi * 5.1 / 180)

    def reverse_kepler(nt, e):
        return nt + (np.sin(nt)) * e + (np.sin(2 * nt) / 2) * (e ** 2) + (-np.sin(nt) / 8 + np.sin(3 * nt) * 3 / 8) * (e ** 3) + (-np.sin(2 * nt) / 6 + np.sin(4 * nt) / 3) * (e ** 4)


    bg_W = np.round(Settings.WIDTH * 2 * np.pi / np.arctan(16 / 9)).astype('i8')
    bg_H = Settings.HEIGHT

    star_bg = Layer(bg_W, bg_H, Settings.FOCAL, Settings.C_U, Settings.C_V, "star background", opaque=True, layer_type=0)

    star_num = 10000
    radT = np.random.rand(star_num) * 2 * np.pi
    rangeS = np.random.rand(star_num) * np.pi
    radS = (np.random.rand(star_num) * 2 - 1) * rangeS

    star_v = 1000000 * np.stack([np.sin(radS) * np.cos(radT), np.cos(radS), np.sin(radS) * np.sin(radT)], axis=1)

    main_render_enabled = False


    print("Initializing finished")


    def main_loop(sec):
        global main_render_enabled
        # -3.0 ~ -2.5 : black screen
        # -2.5 ~ -2.0 : title appears
        # -2.0 ~  0.0 : title hold
        #  0.0        : render start
        #  0.0 ~  0.5 : title / black screen disappears
        #second = sec - 3
        second = sec - 3

        sun_u = reverse_kepler(2 * np.pi * second / 60, 0.0167)
        sun_pos = np.array([-23063.6 * np.sin(sun_u), 0, 23847.6 * (np.cos(sun_u) - 0.0167)])
        Sun.pos = sun_pos
        sunrotdir = -sun_pos / np.sqrt(np.sum(sun_pos ** 2))

        if sunrotdir[0] > 0:
            sun_rot = 2 * np.pi - np.arccos(sunrotdir[2])
        elif sunrotdir[0] == 0:
            if sunrotdir[2] > 0:
                sun_rot = 0
            else:
                sun_rot = np.pi
        else:
            sun_rot = np.arccos(sunrotdir[2])
        directionallight.set_pos(sun_pos / 200)
        directionallight.set_rot(Quaternion.euler_to_quaternion(0, sun_rot, 0))

        Earth_base.rot = Quaternion.euler_to_quaternion(0, -2 * np.pi * second / 2, np.pi * 23.4 / 180)

        moon_u = reverse_kepler(2 * np.pi * second / 6, 0.0549)
        moon_mainc = 63.58 * (np.cos(moon_u) - 0.0549)
        Moon.pos = np.array([-56.96 * np.sin(moon_u), moon_mainc * moon_s, moon_mainc * moon_c])


        # numbers computed in order of pitch, yaw, roll, written in roll, yaw, pitch
        if second <= 10:
            #cam.pos = directionallight.pos
            #cam.rot = directionallight.rot
            pass
        elif second <= 40:
            camdeg = -np.pi / 6 * np.sin(2 * np.pi * (second - 10) / 30)
            if second <= 12:
                camdeg *= (second - 10) / 2
            elif 38 < second:
                camdeg *= (40 - second) / 2
            cam.rot = Quaternion.euler_to_quaternion(0, camdeg, 0)
            cam.pos = np.array([30 * np.sin(camdeg), 0, -30 * np.cos(camdeg)])
            #cam.pos = directionallight.pos
            #cam.rot = directionallight.rot
        elif second <= 50:
            t = (-np.cos(np.pi * (second - 40) / 10) + 1) / 2
            cam.rot = Quaternion.euler_to_quaternion(-np.pi / 12 * t, 0, 0)
            cam.pos = np.array([0, 0, -30,]) * (1 - t) + np.array([0, 30, -111.96]) * t
        else:
            cam.rot = Quaternion.euler_to_quaternion(-np.pi / 12, 0, 0)
            cam.pos = np.array([0, 30, -111.96])

        
        R = cam.rot.matrix
        T = -np.matmul(cam.rot.matrix, cam.pos.reshape(3, 1))
        new_star_v = ShaderVertex.transform_world_to_camera(R, T, star_v)
        star_depth_filter = 10 <= new_star_v[2, :]
        new_star_v, _ = ShaderVertex.transform_camera_to_canvas(Settings.FOCAL, Settings.C_U, Settings.C_V, new_star_v[:, star_depth_filter], False)
        star_side_filter = np.logical_and(np.logical_and(0 <= new_star_v[0], new_star_v[0] <= Settings.WIDTH), np.logical_and(0 <= new_star_v[1], new_star_v[1] <= Settings.HEIGHT))
        new_star_v = new_star_v[:, star_side_filter].astype('i8')
        canvas.bg_layer.img = np.tile(np.array([0, 0, 0, 255], dtype='u1').reshape(1, 1, 4), (Settings.WIDTH, Settings.HEIGHT, 1))
        canvas.bg_layer.img[new_star_v[0], new_star_v[1], :] = 255


        if second <= -2.5:
            canvas.front_layer.img = np.tile(np.array([0, 0, 0, 255], dtype='u1').reshape(1, 1, 4), (canvas.W, canvas.H, 1))
        elif second <= -2:
            canvas.front_layer.img = np.tile(np.array([0, 0, 0, 255], dtype='u1').reshape(1, 1, 4), (canvas.W, canvas.H, 1))
            Text2D.text(canvas.front_layer, 320, 120, "地球", Color.RGB_to_color(255, 255, 255, 255 * (2.5 + second) * 2), size=4, text_align='c')
            Text2D.text(canvas.front_layer, 320, 160, "(と太陽と月)", Color.RGB_to_color(255, 255, 255, 255 * (2.5 + second) * 2), size=2, text_align='c')
            Text2D.text(canvas.front_layer, 320, 260, "Земля", Color.RGB_to_color(255, 255, 255, 255 * (2.5 + second) * 2), size=4, text_align='c')
            Text2D.text(canvas.front_layer, 320, 300, "(и Солнце, и Луна)", Color.RGB_to_color(255, 255, 255, 255 * (2.5 + second) * 2), size=2, text_align='c')
        elif second <= 0:
            canvas.front_layer.img = np.tile(np.array([0, 0, 0, 255], dtype='u1').reshape(1, 1, 4), (canvas.W, canvas.H, 1))
            Text2D.text(canvas.front_layer, 320, 120, "地球", Color.RGB_to_color(255, 255, 255, 255), size=4, text_align='c')
            Text2D.text(canvas.front_layer, 320, 160, "(と太陽と月)", Color.RGB_to_color(255, 255, 255, 255), size=2, text_align='c')
            Text2D.text(canvas.front_layer, 320, 260, "Земля", Color.RGB_to_color(255, 255, 255, 255), size=4, text_align='c')
            Text2D.text(canvas.front_layer, 320, 300, "(и Солнце, и Луна)", Color.RGB_to_color(255, 255, 255, 255), size=2, text_align='c')
        elif second <= 0.5:
            main_render_enabled = True
            canvas.front_layer.img = np.tile(np.array([0, 0, 0, 255], dtype='u1').reshape(1, 1, 4), (canvas.W, canvas.H, 1))
            Text2D.text(canvas.front_layer, 320, 120, "地球", Color.RGB_to_color(255, 255, 255, 255), size=4, text_align='c')
            Text2D.text(canvas.front_layer, 320, 160, "(と太陽と月)", Color.RGB_to_color(255, 255, 255, 255), size=2, text_align='c')
            Text2D.text(canvas.front_layer, 320, 260, "Земля", Color.RGB_to_color(255, 255, 255, 255), size=4, text_align='c')
            Text2D.text(canvas.front_layer, 320, 300, "(и Солнце, и Луна)", Color.RGB_to_color(255, 255, 255, 255), size=2, text_align='c')
            canvas.front_layer.img[:, :, 3] = round(255 - second * 510)
        elif second <= 60:
            canvas.front_layer.img = np.zeros((canvas.W, canvas.H, 4), dtype='u1')
        else:
            canvas.front_layer.img = np.tile(np.array([0, 0, 0, 255], dtype='u1').reshape(1, 1, 4), (canvas.W, canvas.H, 1))
            canvas.front_layer.img[:, :, 3] = round((second - 60) * 255)

        return

    print("Rendering...")

    max_frame = round(max_time * Settings.FPS)

    for i in range(max_frame):
        print("Frame {:5d} / {:5d} ... ".format(i + 1, max_frame), end='')
        time_sta = time.perf_counter()
        canvas.clear_layers()

        main_loop(i / Settings.FPS)

        if main_render_enabled:
            shadows, time_ini, time_sha, time_end = GraphicsPipeline.run(canvas, cam, world)
            shadows_list.append(shadows)
        else:
            time_ini = time.perf_counter()
            time_sha = time.perf_counter()
            time_end = time.perf_counter()

        res = AntiAliasing.SSAA_grid(canvas.output_mixed_layers(), Settings.SSAA_RATIO).transpose(1, 0, 2)

        print("init: {:12.9f}, shad: {:12.9f}, main: {:12.9f}".format(time_ini - time_sta, time_sha - time_ini, time_end - time_sha))

        im = ax.imshow(res, animated=True, aspect='auto')
        if i == 0:
            ax.imshow(res)
        imgs.append([im])

    print("Rendering finished")
