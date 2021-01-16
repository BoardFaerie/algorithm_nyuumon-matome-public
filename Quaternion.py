class Quaternion:
    """Quaternion class for rotation"""
    # https://ja.wikipedia.org/wiki/四元数
    # https://en.wikipedia.org/wiki/Quaternion
    # https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
    # https://qiita.com/mebiusbox2/items/2fa0f0a9ca1cf2044e82
    # https://qiita.com/drken/items/0639cf34cce14e8d58a5
    # https://kamino.hatenablog.com/entry/rotation_expressions

    def __init__(self, w, x, y, z):
        self._w = w
        self._v = np.array([x, y, z])

    @property
    def abs(self):
        return np.sqrt(self._w ** 2 + np.sum(self._v ** 2))

    @property
    def abssqrd(self):
        return self._w ** 2 + np.sum(self._v ** 2)

    @property
    def con(self):
        return self.conjucate

    @property
    def conjugate(self):
        v = -self._v
        return Quaternion(self._w, v[0], v[1], v[2])

    @property
    def inv(self):
        return self.inverse

    @property
    def inverse(self):
        return self.conjugate / self.abssqrd

    @property
    def matrix(self):
        x = self._v[0]
        y = self._v[1]
        z = self._v[2]
        w = self._w
        return np.array([
            [x ** 2 - y ** 2 - z ** 2 + w ** 2, 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), - x ** 2 + y ** 2 - z ** 2 + w ** 2, 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), - x ** 2 - y ** 2 + z ** 2 + w ** 2]
        ])

    def __add__(self, other):
        v = self._v + other._v
        return Quaternion(self._w + other._w, v[0], v[1], v[2])

    def __sub__(self, other):
        v = self._v - other._v
        return Quaternion(self._w - other._w, v[0], v[1], v[2])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            v = self._v * other
            return Quaternion(self._w * other, v[0], v[1], v[2])
        elif isinstance(other, Quaternion):
            return Quaternion.mul(self, other)
        else:
            return 0

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            v = self._v / other
            return Quaternion(self._w / other, v[0], v[1], v[2])
        else:
            return 0

    def __eq__(self, other):
        if isinstance(other, Quaternion):
            return np.all(self._v == other._v) and self._w == other._w
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Quaternion):
            return np.any(self._v != other._v) or self._w != other._w
        else:
            return True

    def __iadd__(self, other):
        self._v += other._v
        self._w += other._w
        return self

    def __isub__(self, other):
        self._v -= other._v
        self._w -= other._w
        return self

    def __imul__(self, other):
        if isinstance(other, (int, float)):
            self._v *= other
            self._w *= other
            return self
        elif isinstance(other, Quaternion):
            self = Quaternion.mul(self, other)
            return self
        else:
            return 0

    def __itruediv__(self, other):
        if isinstance(other, (int, float)):
            v = self._v / other
            return Quaternion(self._w / other, v[0], v[1], v[2])
        else:
            return 0

    def __str__(self):
        return str(np.array([self._w, self._v[0], self._v[1], self._v[2]]))

    def normalize(self):
        self /= self.abs

    @staticmethod
    def mul(q1, q2):
        v = q1._w * q2._v + q2._w * q1._v + np.cross(q1._v, q2._v)
        return Quaternion(q1._w * q2._w - np.inner(q1._v, q2._v), v[0], v[1], v[2])

    @staticmethod
    def vector(v):
        return Quaternion(0, v[0], v[1], v[2])

    @staticmethod
    def rotate_quaternion_with_quaternion(p, q):
        return Quaternion.mul(Quaternion.mul(q, p), q.inv)

    @staticmethod
    def rotation_quaternion(n, theta):
        v = np.sin(theta / 2) * n
        return Quaternion(np.cos(theta / 2), v[0], v[1], v[2])

    @staticmethod
    def rotate_vector_with_vector_theta(r, n, theta):
        return Quaternion.rotate_quaternion_with_quaternion(Quaternion.vector(r), Quaternion.rotation_quaternion(n, theta))

    @staticmethod
    def euler_to_quaternion(roll, pitch, yaw):
        cos_roll = np.cos(roll / 2)
        sin_roll = np.sin(roll / 2)
        cos_pitch = np.cos(pitch / 2)
        sin_pitch = np.sin(pitch / 2)
        cos_yaw = np.cos(yaw / 2)
        sin_yaw = np.sin(yaw / 2)

        return Quaternion(
            cos_roll * cos_pitch * cos_yaw + sin_roll * sin_pitch * sin_yaw,
            sin_roll * cos_pitch * cos_yaw - cos_roll * sin_pitch * sin_yaw,
            cos_roll * sin_pitch * cos_yaw + sin_roll * cos_pitch * sin_yaw,
            cos_roll * cos_pitch * sin_yaw - sin_roll * sin_pitch * cos_yaw)

    @staticmethod
    def interpolate(t, q1, q2):
        q1 = q1 / q1.abs
        q2 = q2 / q2.abs
        if q1 == q2:
            return q1
        inner = q1._w * q2._w + np.inner(q1._v, q2._v)
        if inner < 0:
            q2 = -q2
            inner = -inner
        theta = np.arccos(inner)
        return (q1 * np.sin((1 - t) * theta) + q2 * np.sin(t * theta)) / np.sin(theta)
