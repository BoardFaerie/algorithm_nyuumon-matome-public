class Canvas:
    """Canvas class for drawing"""

    def __init__(self, W: int, H: int, name="Default Canvas"):
        self.W = W
        self.H = H
        self.name = name
        self.clear_layers()

    def output_mixed_layers(self):
        final_layer_img = self.bg_layer.img.copy()
        x = np.arange(self.W)
        y = np.arange(self.H)
        xx, yy = np.meshgrid(x, y)
        xx = xx.reshape(-1)
        yy = yy.reshape(-1)
        final_layer_img[xx, yy] = Color.over(self.front_layer.img[xx, yy], Color.over(self.main_layer.img[xx, yy], self.bg_layer.img[xx, yy]))
        return final_layer_img

    def clear_layers(self):
        self.bg_layer = Layer(self.W, self.H, Settings.FOCAL, Settings.C_U, Settings.C_V, "background", opaque=True, layer_type=0)
        self.main_layer = Layer(self.W, self.H, Settings.FOCAL, Settings.C_U, Settings.C_V, "main", opaque=False, layer_type=1)
        self.front_layer = Layer(self.W, self.H, Settings.FOCAL, Settings.C_U, Settings.C_V, "front", opaque=False, layer_type=0)
