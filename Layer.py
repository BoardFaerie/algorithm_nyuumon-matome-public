class Layer:
    """Layer class for canvas class"""

    def __init__(self, W: int, H: int, f=None, c_u:int=None, c_v:int=None, name="Default Layer", opaque=False, layer_type=0):
        self.W = W
        self.H = H
        self.f = f
        self.c_u = c_u
        self.c_v = c_v
        self.name = name
        self.layer_type = layer_type

        if layer_type == 0:
            if opaque:
                self.img = np.tile(np.array([0, 0, 0, 255], dtype='u1').reshape(1, 1, 4), (W, H, 1))
            else:
                self.img = np.full((W, H, 4), 0, dtype='u1')
        elif layer_type == 1:
            if opaque:
                self.img = np.full((W, H, 4), 255, dtype='u1')
            else:
                self.img = np.full((W, H, 4), 0, dtype='u1')
            self.z_buffer = np.zeros((W, H), dtype='f8')
        elif layer_type == 2:
            self.z_buffer = np.zeros((W, H), dtype='f8')

    def save_pos_rot(self, pos, rot):
        self.pos = pos
        self.rot = rot

        self.R = self.rot.matrix
        self.Rinv = self.rot.inv.matrix
        self.T = -np.matmul(self.rot.matrix, self.pos.reshape(3, 1))
        self.Tinv = self.pos.reshape(3, 1)

    def draw_point(self, x, y, c=None, z=None, n=None, lights=None, shadows=None, wire_frame=False):
        if c is not None:
            c = c.reshape(1, -1)
        if z is not None:
            z = np.array([z])
        if n is not None:
            n = n.reshape(1, -1)
        self.draw(np.array([x]), np.array([y]), c, z, n, lights, shadows, wire_frame)

    def draw(self, x, y, c=None, z=None, n=None, lights=None, shadows=None, wire_frame=False):
        xyfilter = np.logical_and(np.logical_and(0 <= x, x < self.W), np.logical_and(0 <= y, y < self.H))
        x = x[xyfilter]
        if x.size > 0:
            y = y[xyfilter]
            z = z[xyfilter]

            if self.layer_type == 0:
                self.img[x, y] = np.clip(c, 0, 255).astype('u1')
            elif self.layer_type == 1:
                zfilter = self.z_buffer[x, y] < z
                x = x[zfilter]
                if x.size > 0:
                    y = y[zfilter]
                    c = c[xyfilter][zfilter]
                    z = z[zfilter]
                    n = n[xyfilter][zfilter]

                    self.z_buffer[x, y] = z
                    light_col = np.tile(Color.clear_color.reshape(1, -1), (x.size, 1)) # row vector
                    P = Raytracing.transform_canvas_to_world(self.f, self.c_u, self.c_v, self.Rinv, self.Tinv, np.concatenate([x.reshape(1, -1), y.reshape(1, -1)], axis=0), z) # column vector

                    for lightid in range(len(lights)):
                        light = lights[lightid]
                        shadow = shadows[lightid]

                        if light.light_type == 0:
                            light_col = Color.add(light_col, light.calc(P, n, self.pos, c=c))
                        elif light.light_type == 1:
                            v = ShaderVertex.transform_world_to_camera(light.R, light.T, P.T)
                            vfilter = np.logical_and(Settings.LIGHT_NEARCLIP <= v[2], v[2] <= Settings.LIGHT_FARCLIP)
                            v = v[:, vfilter]
                            if v.size > 0:
                                newv, dist = ShaderVertex.transform_camera_to_canvas(shadow.f, shadow.c_u, shadow.c_v, v, False)
                                newvfilter = np.logical_and(np.logical_and(0 <= newv[0], newv[0] < shadow.W), np.logical_and(0 <= newv[1], newv[1] < shadow.H))
                                newv = newv[:, newvfilter]
                                if newv.size > 0:
                                    newv = newv.astype('i8')
                                    vfilter[vfilter] = newvfilter
                                    light_col[vfilter] = Color.add(light_col[vfilter], light.calc(P[:, vfilter], n[vfilter], self.pos, dist[newvfilter], shadow.z_buffer[newv[0], newv[1]], c[vfilter], wire_frame))
                        else:
                            v = ShaderVertex.transform_world_to_camera(light.R, light.T, P.T)
                            vfilter = np.logical_and(Settings.LIGHT_NEARCLIP <= v[2], v[2] <= Settings.LIGHT_FARCLIP)
                            v = v[:, vfilter]
                            if v.size > 0:
                                newv, dist = ShaderVertex.transform_camera_to_canvas(shadow.f, shadow.c_u, shadow.c_v, v, True)
                                newvfilter = np.logical_and(np.logical_and(0 <= newv[0], newv[0] < shadow.W), np.logical_and(0 <= newv[1], newv[1] < shadow.H))
                                newv = newv[:, newvfilter]
                                if newv.size > 0:
                                    newv = newv.astype('i8')
                                    vfilter[vfilter] = newvfilter
                                    light_col[vfilter] = Color.add(light_col[vfilter], light.calc(P[:, vfilter], n[vfilter], self.pos, dist[newvfilter], shadow.z_buffer[newv[0], newv[1]], c[vfilter], wire_frame))
                    self.img[x, y] = Color.over(light_col, self.img[x, y])
            else:
                zfilter = self.z_buffer[x, y] < z
                x = x[zfilter]
                if x.size > 0:
                    y = y[zfilter]
                    self.z_buffer[x, y] = z[zfilter]
