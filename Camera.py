class Camera:
    """Camera in 3D world"""

    def __init__(self, pos=np.array([0, 0, 0]), rot=Quaternion.euler_to_quaternion(0, 0, 0), ortho=False):
        self.pos = pos
        self.rot = rot
        self.ortho = ortho
