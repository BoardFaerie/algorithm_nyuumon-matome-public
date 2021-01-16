class WorldObject:
    """Object in World"""
    # https://yttm-work.jp/model_render/model_render_0001.html
    # https://en.wikipedia.org/wiki/Wavefront_.obj_file

    def __init__(self, pos=np.array([0, 0, 0]), rot=Quaternion.euler_to_quaternion(0, 0, 0), wire_frame=False, enable_shadow=True):
        self.pos = pos
        self.rot = rot
        self.wire_frame = wire_frame
        self.enable_shadow = enable_shadow
        self.vertices = np.array([[]])
        self.arrv = [] # vertices
        self.arrvn = [] # vertex normals
        self.arrtn = [] # face normals
        self.arrtm = [] # face materials

    def triangle_mesh(self, a:int, b:int, c:int, material, normal=None):
        # counter clockwise!
        trinormal = np.cross(self.vertices[c].T - self.vertices[a].T, self.vertices[b].T - self.vertices[a].T).reshape(-1, 1)
        if np.sum(trinormal ** 2) == 0:
            trinormal = np.array([1, 0, 0]).reshape(-1, 1)
        else:
            trinormal = trinormal / np.sqrt(np.sum(trinormal ** 2))
        if normal is None:
            normal = np.concatenate([trinormal.copy(), trinormal.copy(), trinormal.copy()], axis=1)
        self.arrv.append(np.concatenate([self.vertices[a].reshape(-1, 1), self.vertices[b].reshape(-1, 1), self.vertices[c].reshape(-1, 1)], axis=1))
        self.arrvn.append(normal)
        self.arrtn.append(trinormal.reshape(-1))
        self.arrtm.append(material)

    @property
    def v(self):
        return np.array(self.arrv)

    @property
    def vn(self):
        return np.array(self.arrvn)

    @property
    def tn(self):
        return np.array(self.arrtn)

    @property
    def tm(self):
        return np.array(self.arrtm)

    # wire frame objects
    @staticmethod
    def line3D(pos1=np.array([0, 0, 0]), pos2=np.array([0, 0, 0]), material=Material.plastic_lightgray, enable_shadow=True):
        obj = WorldObject(pos, rot, True, enable_shadow)
        obj.vertices = np.concatenate([pos1.reshape(1, -1), pos2.reshape(1, -1)], axis=0)
        obj.triangle_mesh(0, 1, 1, material)
        return obj

    # flat objects
    @staticmethod
    def triangle3D(pos1=np.array([0, 0, 0]), pos2=np.array([0, 0, 0]), pos3=np.array([0, 0, 0]), material=Material.plastic_lightgray, wire_frame=False, enable_shadow=True):
        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        obj.vertices = np.concatenate([pos1.reshape(1, -1), pos2.reshape(1, -1), pos3.reshape(1, -1)], axis=0)
        obj.triangle_mesh(0, 1, 2, material)
        obj.triangle_mesh(0, 2, 1, material)
        return obj

    @staticmethod
    def rectangle3D(pos=np.array([0, 0, 0]), size=np.array([5, 5, 5]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=Material.plastic_lightgray, wire_frame=False, enable_shadow=True):
        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        grid = np.array([[-1, 0, -1], [1, 0, -1], [-1, 0, 1], [1, 0, 1]])
        obj.vertices = np.matmul(grid, np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))
        obj.triangle_mesh(2, 0, 3, material)
        obj.triangle_mesh(2, 3, 0, material)
        obj.triangle_mesh(0, 1, 3, material)
        obj.triangle_mesh(0, 3, 1, material)
        return obj

    @staticmethod
    def regular_polygon3D(pos=np.array([0, 0, 0]), size=np.array([10, 10, 10]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=Material.plastic_lightgray, div=10, wire_frame=False, enable_shadow=True):
        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        a = 2 * np.pi * np.arange(div).reshape(-1, 1) / div
        grid_outer = np.concatenate([np.cos(a), np.zeros((div, 1)), np.sin(a)], axis=1)
        grid = np.concatenate([np.array([[0, 0, 0]]), grid_outer], axis=0)
        obj.vertices = np.matmul(grid, np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))

        for i in range(1, div):
            if wire_frame:
                obj.triangle_mesh(i, i, i + 1, material)
            else:
                obj.triangle_mesh(0, i, i + 1, material)
        if wire_frame:
            obj.triangle_mesh(div, div, 1, material)
        else:
            obj.triangle_mesh(0, div, 1, material)
        return obj

    # volumetric objects
    @staticmethod
    def cube3D(pos=np.array([0, 0, 0]), size=np.array([5, 5, 5]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=np.tile(Material.plastic_lightgray.reshape(1, -1), (6, 1)), wire_frame=False, enable_shadow=True):
        # https://en.wikipedia.org/wiki/Cube

        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        grid = np.array([[-1, 1, -1], [1, 1, -1], [-1, 1, 1], [1, 1, 1], [-1, -1, -1], [1, -1, -1], [-1, -1, 1], [1, -1, 1]])
        obj.vertices = np.matmul(grid, np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))
        obj.triangle_mesh(0, 4, 1, material[0])
        obj.triangle_mesh(4, 5, 1, material[0])
        obj.triangle_mesh(1, 5, 3, material[1])
        obj.triangle_mesh(5, 7, 3, material[1])
        obj.triangle_mesh(3, 7, 2, material[2])
        obj.triangle_mesh(7, 6, 2, material[2])
        obj.triangle_mesh(2, 6, 0, material[3])
        obj.triangle_mesh(6, 4, 0, material[3])
        obj.triangle_mesh(2, 0, 3, material[4])
        obj.triangle_mesh(0, 1, 3, material[4])
        obj.triangle_mesh(4, 6, 5, material[5])
        obj.triangle_mesh(6, 7, 5, material[5])
        return obj

    @staticmethod
    def tetrahedron3D(pos=np.array([0, 0, 0]), size=np.array([10, 10, 10]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=np.tile(Material.plastic_lightgray.reshape(1, -1), (4, 1)), wire_frame=False, enable_shadow=True):
        # https://en.wikipedia.org/wiki/Tetrahedron

        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        a = np.sqrt(3)
        b = np.sqrt(6)
        grid = np.array([[0, b / 3, 0], [0, 0, a / 3], [0.5, 0, -a / 6], [-0.5, 0, -a / 6]])
        obj.vertices = np.matmul(grid, np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))
        obj.triangle_mesh(0, 2, 1, material[0])
        obj.triangle_mesh(0, 3, 2, material[1])
        obj.triangle_mesh(0, 1, 3, material[2])
        obj.triangle_mesh(1, 2, 3, material[3])
        return obj

    @staticmethod
    def octahedron3D(pos=np.array([0, 0, 0]), size=np.array([5, 5, 5]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=np.tile(Material.plastic_lightgray.reshape(1, -1), (8, 1)), wire_frame=False, enable_shadow=True):
        # https://en.wikipedia.org/wiki/Octahedron

        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        grid = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1], [-1, 0, 0], [0, 0, -1], [0, -1, 0]])
        obj.vertices = np.matmul(grid, np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))
        obj.triangle_mesh(0, 1, 2, material[0])
        obj.triangle_mesh(0, 2, 3, material[1])
        obj.triangle_mesh(0, 3, 4, material[2])
        obj.triangle_mesh(0, 4, 1, material[3])
        obj.triangle_mesh(1, 5, 2, material[4])
        obj.triangle_mesh(2, 5, 3, material[5])
        obj.triangle_mesh(3, 5, 4, material[6])
        obj.triangle_mesh(4, 5, 1, material[7])
        return obj

    @staticmethod
    def icosahedron3D(pos=np.array([0, 0, 0]), size=np.array([10, 10, 10]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=np.tile(Material.plastic_lightgray.reshape(1, -1), (20, 1)), wire_frame=False, enable_shadow=True):
        # https://en.wikipedia.org/wiki/Regular_icosahedron

        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        s = 1 / np.sqrt(5)
        c = 2 / np.sqrt(5)
        a = np.pi * 2 / 5
        b = np.pi / 5
        grid = np.array([[0, 1, 0], [c * np.cos(a), s, c * np.sin(a)], [c * np.cos(a * 2), s, c * np.sin(a * 2)], [c * np.cos(a * 3), s, c * np.sin(a * 3)], [c * np.cos(a * 4), s, c * np.sin(a * 4)], [c, s, 0], [c * np.cos(b), -s, c * np.sin(b)], [c * np.cos(b + a), -s, c * np.sin(b + a)], [c * np.cos(b + a * 2), -s, c * np.sin(b + a * 2)], [c * np.cos(b + a * 3), -s, c * np.sin(b + a * 3)], [c * np.cos(b + a * 4), -s, c * np.sin(b + a * 4)], [0, -1, 0]])
        obj.vertices = np.matmul(grid, np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))
        obj.triangle_mesh(0, 1, 2, material[0])
        obj.triangle_mesh(0, 2, 3, material[1])
        obj.triangle_mesh(0, 3, 4, material[2])
        obj.triangle_mesh(0, 4, 5, material[3])
        obj.triangle_mesh(0, 5, 1, material[4])
        obj.triangle_mesh(1, 6, 7, material[5])
        obj.triangle_mesh(1, 7, 2, material[6])
        obj.triangle_mesh(2, 7, 8, material[7])
        obj.triangle_mesh(2, 8, 3, material[8])
        obj.triangle_mesh(3, 8, 9, material[9])
        obj.triangle_mesh(3, 9, 4, material[10])
        obj.triangle_mesh(4, 9, 10, material[11])
        obj.triangle_mesh(4, 10, 5, material[12])
        obj.triangle_mesh(5, 10, 6, material[13])
        obj.triangle_mesh(5, 6, 1, material[14])
        obj.triangle_mesh(6, 11, 7, material[15])
        obj.triangle_mesh(7, 11, 8, material[16])
        obj.triangle_mesh(8, 11, 9, material[17])
        obj.triangle_mesh(9, 11, 10, material[18])
        obj.triangle_mesh(10, 11, 6, material[19])
        return obj

    @staticmethod
    def prism3D(pos=np.array([0, 0, 0]), size=np.array([10, 10, 10]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=np.tile(Material.plastic_lightgray.reshape(1, -1), (3, 1)), div=10, wire_frame=False, enable_shadow=True):
        # https://en.wikipedia.org/wiki/Prism_(geometry)
        # https://en.wikipedia.org/wiki/Cylinder

        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        a = 2 * np.pi * np.arange(div).reshape(-1, 1) / div
        gridtop = np.concatenate([np.cos(a), np.ones((div, 1)), np.sin(a)], axis=1)
        gridbottom = gridtop.copy()
        gridbottom[:, 1] = 0
        grid = np.concatenate([np.array([[0, 1, 0]]), gridtop, np.array([[0, 0, 0]]), gridbottom], axis=0)
        obj.vertices = np.matmul(grid, np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))

        for i in range(1, div):
            obj.triangle_mesh(0, i, i + 1, material[0])
        obj.triangle_mesh(0, div, 1, material[0])
        for i in range(div + 2, 2 * div + 1):
            obj.triangle_mesh(div + 1, i + 1, i, material[1])
        obj.triangle_mesh(div + 1, div + 2, 2 * div + 1, material[1])
        for i in range(1, div):
            obj.triangle_mesh(i, div + i + 1, i + 1, material[2])
            obj.triangle_mesh(div + i + 1, div + i + 2, i + 1, material[2])
        obj.triangle_mesh(div, 2 * div + 1, 1, material[2])
        obj.triangle_mesh(2 * div + 1, div + 2, 1, material[2])
        return obj

    @staticmethod
    def pyramid3D(pos=np.array([0, 0, 0]), size=np.array([10, 10, 10]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=np.tile(Material.plastic_lightgray.reshape(1, -1), (3, 1)), div=10, wire_frame=False, enable_shadow=True):
        # https://en.wikipedia.org/wiki/Pyramid_(geometry)
        # https://en.wikipedia.org/wiki/Cone

        obj = WorldObject(pos, rot, wire_frame, enable_shadow)
        a = 2 * np.pi * np.arange(div).reshape(-1, 1) / div
        gridbottom = np.concatenate([np.cos(a), np.zeros((div, 1)), np.sin(a)], axis=1)
        grid = np.concatenate([np.array([[0, 0, 0]]), np.array([[0, 1, 0]]), gridbottom], axis=0)
        obj.vertices = np.matmul(grid, np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))

        for i in range(2, div + 1):
            obj.triangle_mesh(0, i + 1, i, material[0])
        obj.triangle_mesh(0, 2, div + 1, material[0])
        for i in range(2, div + 1):
            obj.triangle_mesh(1, i, i + 1, material[1])
        obj.triangle_mesh(1, div + 1, 2, material[1])
        return obj

    @staticmethod
    def sphere3D(pos=np.array([0, 0, 0]), size=np.array([10, 10, 10]), rot=Quaternion.euler_to_quaternion(0, 0, 0), material=np.tile(Material.plastic_lightgray.reshape(1, -1), (80, 1)), div=1, smooth=True, wire_frame=False, enable_shadow=True):
        # https://en.wikipedia.org/wiki/Sphere

        obj = WorldObject.icosahedron3D(pos, size, rot, wire_frame=wire_frame, enable_shadow=enable_shadow)
        for i in range(div):
            if smooth:
                for trinum in range(len(obj.arrvn)):
                    obj.arrvn[trinum][:, 0] = obj.arrv[trinum][:, 0] / np.sqrt(np.sum(obj.arrv[trinum][:, 0] ** 2))
                    obj.arrvn[trinum][:, 1] = obj.arrv[trinum][:, 1] / np.sqrt(np.sum(obj.arrv[trinum][:, 1] ** 2))
                    obj.arrvn[trinum][:, 2] = obj.arrv[trinum][:, 2] / np.sqrt(np.sum(obj.arrv[trinum][:, 2] ** 2))

            WorldObject.tessellate_double(obj)
            for trinum in range(len(obj.arrvn)):
                obj.arrv[trinum][:, 0] = np.matmul(obj.arrv[trinum][:, 0] / np.sqrt(np.sum(obj.arrv[trinum][:, 0] ** 2)), np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))
                obj.arrv[trinum][:, 1] = np.matmul(obj.arrv[trinum][:, 1] / np.sqrt(np.sum(obj.arrv[trinum][:, 1] ** 2)), np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))
                obj.arrv[trinum][:, 2] = np.matmul(obj.arrv[trinum][:, 2] / np.sqrt(np.sum(obj.arrv[trinum][:, 2] ** 2)), np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]]))

        findiv = round(20 * np.exp2(2 * div))
        assert(material.shape[0] >= findiv)
        obj.arrtm = material[0:20 * findiv]
        return obj

    @staticmethod
    def tessellate_double(obj, material_copy=False):
        new_arrv = []
        new_arrvn = []
        new_arrtn = []
        if material_copy:
            new_arrtm = []

        for trinum in range(len(obj.arrv)):
            A = obj.arrv[trinum][:, 0].copy().reshape(-1, 1)
            B = obj.arrv[trinum][:, 1].copy().reshape(-1, 1)
            C = obj.arrv[trinum][:, 2].copy().reshape(-1, 1)

            new_arrv.append(np.concatenate([A, (A + B) / 2, (A + C) / 2], axis=1))
            new_arrv.append(np.concatenate([(A + B) / 2, (B + C) / 2, (A + C) / 2], axis=1))
            new_arrv.append(np.concatenate([(A + C) / 2, (B + C) / 2, C], axis=1))
            new_arrv.append(np.concatenate([(A + B) / 2, B, (B + C) / 2], axis=1))

            An = obj.arrvn[trinum][:, 0].copy().reshape(-1, 1)
            Bn = obj.arrvn[trinum][:, 1].copy().reshape(-1, 1)
            Cn = obj.arrvn[trinum][:, 2].copy().reshape(-1, 1)

            new_arrvn.append(np.concatenate([An, (An + Bn) / 2, (An + Cn) / 2], axis=1))
            new_arrvn.append(np.concatenate([(An + Bn) / 2, (Bn + Cn) / 2, (An + Cn) / 2], axis=1))
            new_arrvn.append(np.concatenate([(An + Cn) / 2, (Bn + Cn) / 2, Cn], axis=1))
            new_arrvn.append(np.concatenate([(An + Bn) / 2, Bn, (Bn + Cn) / 2], axis=1))

            new_arrtn.append(((An * 2 + Bn / 2 + Cn / 2) / 3).reshape(-1))
            new_arrtn.append(((An + Bn + Cn) / 3).reshape(-1))
            new_arrtn.append(((An / 2 + Bn / 2 + Cn * 2) / 3).reshape(-1))
            new_arrtn.append(((An / 2 + Bn * 2 + Cn / 2) / 3).reshape(-1))

            if material_copy:
                new_arrtm.append(obj.arrtm[trinum].copy())
                new_arrtm.append(obj.arrtm[trinum].copy())
                new_arrtm.append(obj.arrtm[trinum].copy())
                new_arrtm.append(obj.arrtm[trinum].copy())

        obj.arrv = new_arrv
        obj.arrvn = new_arrvn
        obj.arrtn = new_arrtn
        if material_copy:
            obj.arrtm = new_arrtm
