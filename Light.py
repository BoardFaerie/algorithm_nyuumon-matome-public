class Light:
    """Light in World"""
    # https://www.gabrielgambetta.com/computer-graphics-from-scratch/shading.html
    # https://en.wikipedia.org/wiki/Phong_reflection_model
    # https://ja.wikipedia.org/wiki/Phongの反射モデル
    # http://www.opengl-tutorial.org/intermediate-tutorials/tutorial-16-shadow-mapping/
    # https://en.wikipedia.org/wiki/Computer_graphics_lighting

    def __init__(self, pos=np.array([0, 0, 0]), rot=Quaternion.euler_to_quaternion(0, 0, 0), light_type=1, intensity=0.1, intensity2=0.4, color=Color.white):
        #type = 0: ambient
        #type = 1: point
        #type = 2: directional
        self.pos = pos
        self.rot = rot
        self.light_type = light_type
        self.intensity = intensity
        self.intensity2 = intensity2
        self.color = color

        self.R = self.rot.matrix
        self.Rinv = self.rot.inv.matrix
        self.T = -np.matmul(self.rot.matrix, self.pos.reshape(3, 1))
        self.Tinv = self.pos.reshape(3, 1)

    def set_pos(self, pos):
        self.pos = pos
        self.T = -np.matmul(self.rot.matrix, self.pos.reshape(3, 1))
        self.Tinv = self.pos.reshape(3, 1)

    def set_rot(self, rot):
        self.rot = rot
        self.R = self.rot.matrix
        self.Rinv = self.rot.inv.matrix
        self.T = -np.matmul(self.rot.matrix, self.pos.reshape(3, 1))

    def calc(self, P, N, campos, dist=None, z_buffer=None, c=None, wire_frame=False):
        if self.light_type == 0:
            return np.clip(np.concatenate([np.tile(self.color[0:3].reshape(1, -1), (c.shape[0], 1)) * self.intensity * c[:, 0:3], c[:, 10].reshape(-1, 1) * 255], axis=1), 0, 255).astype('u1')
        elif self.light_type == 1 or self.light_type == 2:
            if self.light_type == 1:
                L = np.tile(self.pos.reshape(3, 1), (1, P.shape[1])) - P # column vector
            else:
                L = -np.matmul(self.Rinv, np.tile(np.array([0, 0, 1]).reshape(3, 1), (1, P.shape[1]))) # column vector
            L = L / np.sqrt(np.tile(np.sum(L ** 2, axis=0).reshape(1, -1), (3, 1))) # column vector
            if wire_frame:
                N = L.T # row vector
            else:
                N = N / np.sqrt(np.tile(np.sum(N ** 2, axis=1).reshape(-1, 1), (1, 3))) # row vector

            l_n = np.diag(np.matmul(N, L))
            lnfilter = l_n > 0
            l_n = l_n[lnfilter]
            if l_n.size > 0:
                dist = dist[lnfilter]
                z_buffer = z_buffer[lnfilter]
                distfilter = dist >= z_buffer - Settings.EPSILON * np.sqrt(1 / l_n / l_n - 1)
                dist = dist[distfilter]
                if dist.size > 0:
                    l_n = l_n[distfilter]
                    lnfilter[lnfilter] = distfilter
                    P = P[:, lnfilter]
                    N = N[lnfilter]
                    L = L[:, lnfilter]
                    c = c[lnfilter]

                    V = np.tile(campos.reshape(3, 1), (1, P.shape[1])) - P # column vector
                    R = 2 * np.tile(l_n.reshape(-1, 1), (1, 3)) * N - L.T # row vector
                    R = R / np.sqrt(np.tile(np.sum(R ** 2, axis=1).reshape(-1, 1), (1, 3)))
                    V = V / np.sqrt(np.tile(np.sum(V ** 2, axis=0).reshape(1, -1), (3, 1)))
                    r_v = np.diag(np.matmul(R, V))
                    
                    ret = np.zeros((lnfilter.size, 4))
                    ret[lnfilter] = np.clip(np.concatenate([np.tile(self.color[0:3].reshape(1, -1), (c.shape[0], 1)) * (self.intensity * c[:, 3:6] * np.tile(l_n.reshape(-1, 1), (1, 3)) + self.intensity2 * c[:, 6:9] * np.tile(np.power(r_v, c[:, 9]).reshape(-1, 1), (1, 3))), c[:, 10].reshape(-1, 1) * 255], axis=1), 0, 255)
                    return ret
                else:
                    return np.zeros((c.shape[0], 4))
            else:
                return np.zeros((c.shape[0], 4))
        else:
            return np.zeros((c.shape[0], 4))
