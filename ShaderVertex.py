class ShaderVertex:
    """Vertex Shader, for transforming 3D into 2D"""
    #left-handed system!!!
    # https://daily-tech.hatenablog.com/entry/2018/01/22/071346
    # https://daily-tech.hatenablog.com/entry/2018/01/23/064926
    # https://en.wikipedia.org/wiki/Camera_matrix
    # https://en.wikipedia.org/wiki/Vertex_pipeline

    @staticmethod
    def transform_world_to_camera(R, T, v=None, n=None):
        M = np.concatenate([np.concatenate([R, T], 1), np.array([[0, 0, 0, 1]])], 0)
        if v is not None and n is None:
            vdash = np.concatenate([v.T, np.ones((1, v.shape[0]))], 0)
            return np.matmul(M, vdash)[0:3, :]
        elif v is None and n is not None:
            return np.matmul(R, n.T)
        elif v is not None and n is not None:
            vdash = np.concatenate([v.T, np.ones((1, v.shape[0]))], 0)
            return np.matmul(M, vdash)[0:3, :], np.matmul(R, n.T)
        else:
            return None

    @staticmethod
    def transform_camera_to_canvas(f, c_u, c_v, v, ortho=False):
        z_buffer = 1 / v[2, :].copy()
        if ortho:
            v[2, :] = 1
            f /= 100

        A = np.array([[f, 0, c_u],[0, -f, c_v],[0, 0, 1]])
        new_v = np.matmul(A, v)
        scalerow = new_v[2, :].copy()

        return new_v[0:2, :] / np.stack([scalerow, scalerow]), z_buffer
