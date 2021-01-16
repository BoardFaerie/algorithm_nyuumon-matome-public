class Raytracing:
    """Ray Tracing class"""

    @staticmethod
    def transform_camera_to_world(R, T, v):
        M = np.concatenate([np.concatenate([R, T], 1), np.array([[0, 0, 0, 1]])], 0)
        vdash = np.concatenate([v, np.ones((1, v.shape[1]))], axis=0)
        res = np.matmul(M, vdash)
        return res[0:3, :] / np.tile(res[3].reshape(1, -1), (3, 1))

    @staticmethod
    def transform_canvas_to_world(f, c_u, c_v, R, T, v, z_buffer):
        """Transform points on perspective v to normalized ray vectors (X_W, Y_W, Z_W)"""
        # https://www.gabrielgambetta.com/computer-graphics-from-scratch/basic-ray-tracing.html
        vdash = np.concatenate([v, np.ones((1, v.shape[1]))], axis=0)
        Ainv = np.array([[1/f, 0, -c_u/f],[0, -1/f, c_v/f],[0, 0, 1]])
        camera_points = np.matmul(Ainv, vdash) / np.tile(z_buffer.reshape(1, -1), (3, 1))
        return Raytracing.transform_camera_to_world(R, T, camera_points)
