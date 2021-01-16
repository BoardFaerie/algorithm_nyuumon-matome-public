class ShaderGeometry:
    """Geometry Shader, for clipping and tessellation(not implemented)"""
    # https://www.gabrielgambetta.com/computer-graphics-from-scratch/clipping.html
    # https://www.gabrielgambetta.com/computer-graphics-from-scratch/hidden-surface-removal.html
    # https://en.wikipedia.org/wiki/Clipping_(computer_graphics)
    # https://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm
    # https://en.wikipedia.org/wiki/Geometry_pipelines
    # http://www.opengl-tutorial.org/intermediate-tutorials/tutorial-16-shadow-mapping/

    @staticmethod
    def frontface_culling(v1, v2, v3, tn, n1=None, n2=None, n3=None, c=None, wf=None):
        if wf is None:
            front_filter = np.matmul(np.array([0, 0, 1]), tn) >= -Settings.EPSILON
        else:
            front_filter = np.logical_or(np.matmul(np.array([0, 0, 1]), tn) >= -Settings.EPSILON, wf)
        if c is not None:
            return v1[:, front_filter], v2[:, front_filter], v3[:, front_filter], tn[:, front_filter], n1[:, front_filter], n2[:, front_filter], n3[:, front_filter], c[:, front_filter], wf[front_filter]
        else:
            return v1[:, front_filter], v2[:, front_filter], v3[:, front_filter]

    @staticmethod
    def backface_culling(v1, v2, v3, tn, n1=None, n2=None, n3=None, c=None, wf=None):
        if wf is None:
            back_filter = np.matmul(np.array([0, 0, 1]), tn) <= Settings.EPSILON
        else:
            back_filter = np.logical_or(np.matmul(np.array([0, 0, 1]), tn) <= Settings.EPSILON, wf)
        if c is not None:
            return v1[:, back_filter], v2[:, back_filter], v3[:, back_filter], tn[:, back_filter], n1[:, back_filter], n2[:, back_filter], n3[:, back_filter], c[:, back_filter], wf[back_filter]
        else:
            return v1[:, back_filter], v2[:, back_filter], v3[:, back_filter]

    @staticmethod
    def depth_clip(v1, v2, v3, nearclip, farclip, tn=None, n1=None, n2=None, n3=None, c=None, wf=None):
        depth_filter = np.logical_or(np.logical_or(np.logical_and(nearclip <= v1[2, :], v1[2, :] <= farclip), np.logical_and(nearclip <= v2[2, :], v2[2, :] <= farclip)), np.logical_and(nearclip <= v3[2, :], v3[2, :] <= farclip))
        v1 = v1[:, depth_filter]
        v2 = v2[:, depth_filter]
        v3 = v3[:, depth_filter]
        if n1 is not None:
            n1 = n1[:, depth_filter]
            n2 = n2[:, depth_filter]
            n3 = n3[:, depth_filter]
        if c is not None:
            tn = tn[:, depth_filter]
            c = c[:, depth_filter]
            wf = wf[depth_filter]

        M, N = v1.shape
        for i in range(N):
            if v2[2, i] < v1[2, i]:
                v1[:, i], v2[:, i] = v2[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n2[:, i] = n2[:, i].copy(), n1[:, i].copy()
            if v3[2, i] < v1[2, i]:
                v1[:, i], v3[:, i] = v3[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n3[:, i] = n3[:, i].copy(), n1[:, i].copy()
            if v3[2, i] < v2[2, i]:
                v2[:, i], v3[:, i] = v3[:, i].copy(), v2[:, i].copy()
                if n1 is not None:
                    n2[:, i], n3[:, i] = n3[:, i].copy(), n2[:, i].copy()

            if v1[2, i] < nearclip and v2[2, i] < nearclip and nearclip <= v3[2, i]:
                v1[:, i] = (v3[:, i] + (v1[:, i] - v3[:, i]) * (nearclip - v3[2, i]) / (v1[2, i] - v3[2, i])).copy()
                v2[:, i] = (v3[:, i] + (v2[:, i] - v3[:, i]) * (nearclip - v3[2, i]) / (v2[2, i] - v3[2, i])).copy()
                if n1 is not None:
                    n1[:, i] = (n3[:, i] + (n1[:, i] - n3[:, i]) * (nearclip - v3[2, i]) / (v1[2, i] - v3[2, i])).copy()
                    n2[:, i] = (n3[:, i] + (n2[:, i] - n3[:, i]) * (nearclip - v3[2, i]) / (v2[2, i] - v3[2, i])).copy()
            elif v1[2, i] < nearclip and nearclip <= v2[2, i] and nearclip <= v3[2, i]:
                tmpv1 = v2[:, i] + (v1[:, i] - v2[:, i]) * (nearclip - v2[2, i]) / (v1[2, i] - v2[2, i])
                tmpv2 = v3[:, i] + (v1[:, i] - v3[:, i]) * (nearclip - v3[2, i]) / (v1[2, i] - v3[2, i])
                v1[:, i] = tmpv1.copy()
                v1 = np.concatenate([v1, tmpv1.copy().reshape(-1, 1)], axis=1)
                v2 = np.concatenate([v2, tmpv2.copy().reshape(-1, 1)], axis=1)
                v3 = np.concatenate([v3, v3[:, i].copy().reshape(-1, 1)], axis=1)
                if n1 is not None:
                    tmpn1 = n2[:, i] + (n1[:, i] - n2[:, i]) * (nearclip - v2[2, i]) / (v1[2, i] - v2[2, i])
                    tmpn2 = n3[:, i] + (n1[:, i] - n3[:, i]) * (nearclip - v3[2, i]) / (v1[2, i] - v3[2, i])
                    n1[:, i] = tmpn1.copy()
                    n1 = np.concatenate([n1, tmpn1.copy().reshape(-1, 1)], axis=1)
                    n2 = np.concatenate([n2, tmpn2.copy().reshape(-1, 1)], axis=1)
                    n3 = np.concatenate([n3, n3[:, i].copy().reshape(-1, 1)], axis=1)
                if c is not None:
                    tn = np.concatenate([tn, tn[:, i].copy().reshape(-1, 1)], axis=1)
                    c = np.concatenate([c, c[:, i].copy().reshape(3, 1, 11)], axis=1)
                    wf = np.concatenate([wf, np.array([wf[i].copy()])],axis=0)

        M, N = v1.shape
        for i in range(N):
            if v2[2, i] < v1[2, i]:
                v1[:, i], v2[:, i] = v2[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n2[:, i] = n2[:, i].copy(), n1[:, i].copy()
            if v3[2, i] < v1[2, i]:
                v1[:, i], v3[:, i] = v3[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n3[:, i] = n3[:, i].copy(), n1[:, i].copy()
            if v3[2, i] < v2[2, i]:
                v2[:, i], v3[:, i] = v3[:, i].copy(), v2[:, i].copy()
                if n1 is not None:
                    n2[:, i], n3[:, i] = n3[:, i].copy(), n2[:, i].copy()

            if v1[2, i] <= farclip and v2[2, i] <= farclip and farclip < v3[2, i]:
                tmpv1 = v1[:, i] + (v3[:, i] - v1[:, i]) * (farclip - v1[2, i]) / (v3[2, i] - v1[2, i])
                tmpv2 = v2[:, i] + (v3[:, i] - v2[:, i]) * (farclip - v2[2, i]) / (v3[2, i] - v2[2, i])
                v3[:, i] = tmpv1.copy()
                v1 = np.concatenate([v1, tmpv1.copy().reshape(-1, 1)], axis=1)
                v2 = np.concatenate([v2, tmpv2.copy().reshape(-1, 1)], axis=1)
                v3 = np.concatenate([v3, v2[:, i].copy().reshape(-1, 1)], axis=1)
                if n1 is not None:
                    tmpn1 = n1[:, i] + (n3[:, i] - n1[:, i]) * (farclip - v1[2, i]) / (v3[2, i] - v1[2, i])
                    tmpn2 = n2[:, i] + (n3[:, i] - n2[:, i]) * (farclip - v2[2, i]) / (v3[2, i] - v2[2, i])
                    n3[:, i] = tmpn1.copy()
                    n1 = np.concatenate([n1, tmpn1.copy().reshape(-1, 1)], axis=1)
                    n2 = np.concatenate([n2, tmpn2.copy().reshape(-1, 1)], axis=1)
                    n3 = np.concatenate([n3, n2[:, i].copy().reshape(-1, 1)], axis=1)
                if c is not None:
                    tn = np.concatenate([tn, tn[:, i].copy().reshape(-1, 1)], axis=1)
                    c = np.concatenate([c, c[:, i].copy().reshape(3, 1, 11)], axis=1)
                    wf = np.concatenate([wf, np.array([wf[i].copy()])],axis=0)
            elif v1[2, i] <= farclip and farclip < v2[2, i] and farclip < v3[2, i]:
                v2[:, i] = (v1[:, i] + (v2[:, i] - v1[:, i]) * (farclip - v1[2, i]) / (v2[2, i] - v1[2, i])).copy()
                v3[:, i] = (v1[:, i] + (v3[:, i] - v1[:, i]) * (farclip - v1[2, i]) / (v3[2, i] - v1[2, i])).copy()
                if n1 is not None:
                    n2[:, i] = (n1[:, i] + (n2[:, i] - n1[:, i]) * (farclip - v1[2, i]) / (v2[2, i] - v1[2, i])).copy()
                    n3[:, i] = (n1[:, i] + (n3[:, i] - n1[:, i]) * (farclip - v1[2, i]) / (v3[2, i] - v1[2, i])).copy()

        if n1 is not None:
            return v1, v2, v3, tn, n1, n2, n3, c, wf
        else:
            return v1, v2, v3

    @staticmethod
    def side_clip(v1, z1, v2, z2, v3, z3, c_u, c_v, n1=None, n2=None, n3=None, c=None, wf=None):
        topclip = 0
        bottomclip = c_u * 2
        top_down_filter = np.logical_or(np.logical_or(np.logical_and(topclip <= v1[0, :], v1[0, :] <= bottomclip), np.logical_and(topclip <= v2[0, :], v2[0, :] <= bottomclip)), np.logical_and(topclip <= v3[0, :], v3[0, :] <= bottomclip))
        v1 = v1[:, top_down_filter]
        v2 = v2[:, top_down_filter]
        v3 = v3[:, top_down_filter]
        z1 = z1[top_down_filter]
        z2 = z2[top_down_filter]
        z3 = z3[top_down_filter]
        if c is not None:
            n1 = n1[:, top_down_filter]
            n2 = n2[:, top_down_filter]
            n3 = n3[:, top_down_filter]
            c = c[:, top_down_filter]
            wf = wf[top_down_filter]

        leftclip = 0
        rightclip = c_v * 2
        left_right_filter = np.logical_or(np.logical_or(np.logical_and(leftclip <= v1[1, :], v1[1, :] <= rightclip), np.logical_and(leftclip <= v2[1, :], v2[1, :] <= rightclip)), np.logical_and(leftclip <= v3[1, :], v3[1, :] <= rightclip))
        v1 = v1[:, left_right_filter]
        v2 = v2[:, left_right_filter]
        v3 = v3[:, left_right_filter]
        z1 = z1[left_right_filter]
        z2 = z2[left_right_filter]
        z3 = z3[left_right_filter]
        if c is not None:
            n1 = n1[:, left_right_filter]
            n2 = n2[:, left_right_filter]
            n3 = n3[:, left_right_filter]
            c = c[:, left_right_filter]
            wf = wf[left_right_filter]

        M, N = v1.shape
        for i in range(N):
            if v2[0, i] < v1[0, i]:
                v1[:, i], v2[:, i] = v2[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n2[:, i] = n2[:, i].copy(), n1[:, i].copy()
                z1[i], z2[i] = z2[i].copy(), z1[i].copy()
            if v3[0, i] < v1[0, i]:
                v1[:, i], v3[:, i] = v3[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n3[:, i] = n3[:, i].copy(), n1[:, i].copy()
                z1[i], z3[i] = z3[i].copy(), z1[i].copy()
            if v3[0, i] < v2[0, i]:
                v2[:, i], v3[:, i] = v3[:, i].copy(), v2[:, i].copy()
                if n1 is not None:
                    n2[:, i], n3[:, i] = n3[:, i].copy(), n2[:, i].copy()
                z2[i], z3[i] = z3[i].copy(), z2[i].copy()

            if v1[0, i] < topclip and v2[0, i] < topclip and topclip <= v3[0, i]:
                v1[:, i] = (v3[:, i] + (v1[:, i] - v3[:, i]) * (topclip - v3[0, i]) / (v1[0, i] - v3[0, i])).copy()
                z1[i] = (z3[i] + (z1[i] - z3[i]) * (topclip - v3[0, i]) / (v1[0, i] - v3[0, i])).copy()
                v2[:, i] = (v3[:, i] + (v2[:, i] - v3[:, i]) * (topclip - v3[0, i]) / (v2[0, i] - v3[0, i])).copy()
                z2[i] = (z3[i] + (z2[i] - z3[i]) * (topclip - v3[0, i]) / (v2[0, i] - v3[0, i])).copy()
                if n1 is not None:
                    n1[:, i] = (n3[:, i] + (n1[:, i] - n3[:, i]) * (topclip - v3[0, i]) / (v1[0, i] - v3[0, i])).copy()
                    n2[:, i] = (n3[:, i] + (n2[:, i] - n3[:, i]) * (topclip - v3[0, i]) / (v2[0, i] - v3[0, i])).copy()
            elif v1[0, i] < topclip and topclip <= v2[0, i] and topclip <= v3[0, i]:
                tmpv1 = v2[:, i] + (v1[:, i] - v2[:, i]) * (topclip - v2[0, i]) / (v1[0, i] - v2[0, i])
                tmpv2 = v3[:, i] + (v1[:, i] - v3[:, i]) * (topclip - v3[0, i]) / (v1[0, i] - v3[0, i])
                tmpz1 = z2[i] + (z1[i] - z2[i]) * (topclip - v2[0, i]) / (v1[0, i] - v2[0, i])
                tmpz2 = z3[i] + (z1[i] - z3[i]) * (topclip - v3[0, i]) / (v1[0, i] - v3[0, i])
                v1[:, i] = tmpv1.copy()
                z1[i] = tmpz1.copy()
                v1 = np.concatenate([v1, tmpv1.copy().reshape(-1, 1)], axis=1)
                z1 = np.concatenate([z1, tmpz1.copy().reshape(1)])
                v2 = np.concatenate([v2, tmpv2.copy().reshape(-1, 1)], axis=1)
                z2 = np.concatenate([z2, tmpz2.copy().reshape(1)])
                v3 = np.concatenate([v3, v3[:, i].copy().reshape(-1, 1)], axis=1)
                z3 = np.concatenate([z3, z3[i].copy().reshape(1)])
                if c is not None:
                    tmpn1 = n2[:, i] + (n1[:, i] - n2[:, i]) * (topclip - v2[0, i]) / (v1[0, i] - v2[0, i])
                    tmpn2 = n3[:, i] + (n1[:, i] - n3[:, i]) * (topclip - v3[0, i]) / (v1[0, i] - v3[0, i])
                    n1[:, i] = tmpn1.copy()
                    n1 = np.concatenate([n1, tmpn1.copy().reshape(-1, 1)], axis=1)
                    n2 = np.concatenate([n2, tmpn2.copy().reshape(-1, 1)], axis=1)
                    n3 = np.concatenate([n3, n3[:, i].copy().reshape(-1, 1)], axis=1)
                    c = np.concatenate([c, c[:, i].copy().reshape(3, 1, 11)], axis=1)
                    wf = np.concatenate([wf, np.array([wf[i]])], axis=0)

        M, N = v1.shape
        for i in range(N):
            if v2[0, i] < v1[0, i]:
                v1[:, i], v2[:, i] = v2[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n2[:, i] = n2[:, i].copy(), n1[:, i].copy()
                z1[i], z2[i] = z2[i].copy(), z1[i].copy()
            if v3[0, i] < v1[0, i]:
                v1[:, i], v3[:, i] = v3[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n3[:, i] = n3[:, i].copy(), n1[:, i].copy()
                z1[i], z3[i] = z3[i].copy(), z1[i].copy()
            if v3[0, i] < v2[0, i]:
                v2[:, i], v3[:, i] = v3[:, i].copy(), v2[:, i].copy()
                if n1 is not None:
                    n2[:, i], n3[:, i] = n3[:, i].copy(), n2[:, i].copy()
                z2[i], z3[i] = z3[i].copy(), z2[i].copy()

            if v1[0, i] <= bottomclip and v2[0, i] <= bottomclip and bottomclip < v3[0, i]:
                tmpv1 = v1[:, i] + (v3[:, i] - v1[:, i]) * (bottomclip - v1[0, i]) / (v3[0, i] - v1[0, i])
                tmpv2 = v2[:, i] + (v3[:, i] - v2[:, i]) * (bottomclip - v2[0, i]) / (v3[0, i] - v2[0, i])
                tmpz1 = z1[i] + (z3[i] - z1[i]) * (bottomclip - v1[0, i]) / (v3[0, i] - v1[0, i])
                tmpz2 = z2[i] + (z3[i] - z2[i]) * (bottomclip - v2[0, i]) / (v3[0, i] - v2[0, i])
                v3[:, i] = tmpv1.copy()
                z3[i] = tmpz1.copy()
                v1 = np.concatenate([v1, tmpv1.copy().reshape(-1, 1)], axis=1)
                z1 = np.concatenate([z1, tmpz1.copy().reshape(1)])
                v2 = np.concatenate([v2, tmpv2.copy().reshape(-1, 1)], axis=1)
                z2 = np.concatenate([z2, tmpz2.copy().reshape(1)])
                v3 = np.concatenate([v3, v2[:, i].copy().reshape(-1, 1)], axis=1)
                z3 = np.concatenate([z3, z2[i].copy().reshape(1)])
                if c is not None:
                    tmpn1 = n1[:, i] + (n3[:, i] - n1[:, i]) * (bottomclip - v1[0, i]) / (v3[0, i] - v1[0, i])
                    tmpn2 = n2[:, i] + (n3[:, i] - n2[:, i]) * (bottomclip - v2[0, i]) / (v3[0, i] - v2[0, i])
                    n3[:, i] = tmpn1.copy()
                    n1 = np.concatenate([n1, tmpn1.copy().reshape(-1, 1)], axis=1)
                    n2 = np.concatenate([n2, tmpn2.copy().reshape(-1, 1)], axis=1)
                    n3 = np.concatenate([n3, n2[:, i].copy().reshape(-1, 1)], axis=1)
                    c = np.concatenate([c, c[:, i].copy().reshape(3, 1, 11)], axis=1)
                    wf = np.concatenate([wf, np.array([wf[i]])], axis=0)
            elif v1[0, i] <= bottomclip and bottomclip < v2[0, i] and bottomclip < v3[0, i]:
                v2[:, i] = (v1[:, i] + (v2[:, i] - v1[:, i]) * (bottomclip - v1[0, i]) / (v2[0, i] - v1[0, i])).copy()
                z2[i] = (z1[i] + (z2[i] - z1[i]) * (bottomclip - v1[0, i]) / (v2[0, i] - v1[0, i])).copy()
                v3[:, i] = (v1[:, i] + (v3[:, i] - v1[:, i]) * (bottomclip - v1[0, i]) / (v3[0, i] - v1[0, i])).copy()
                z3[i] = (z1[i] + (z2[i] - z1[i]) * (bottomclip - v1[0, i]) / (v3[0, i] - v1[0, i])).copy()
                if n1 is not None:
                    n2[:, i] = (n1[:, i] + (n2[:, i] - n1[:, i]) * (bottomclip - v1[0, i]) / (v2[0, i] - v1[0, i])).copy()
                    n3[:, i] = (n1[:, i] + (n3[:, i] - n1[:, i]) * (bottomclip - v1[0, i]) / (v3[0, i] - v1[0, i])).copy()

        M, N = v1.shape
        for i in range(N):
            if v2[1, i] < v1[1, i]:
                v1[:, i], v2[:, i] = v2[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n2[:, i] = n2[:, i].copy(), n1[:, i].copy()
                z1[i], z2[i] = z2[i].copy(), z1[i].copy()
            if v3[1, i] < v1[1, i]:
                v1[:, i], v3[:, i] = v3[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n3[:, i] = n3[:, i].copy(), n1[:, i].copy()
                z1[i], z3[i] = z3[i].copy(), z1[i].copy()
            if v3[1, i] < v2[1, i]:
                v2[:, i], v3[:, i] = v3[:, i].copy(), v2[:, i].copy()
                if n1 is not None:
                    n2[:, i], n3[:, i] = n3[:, i].copy(), n2[:, i].copy()
                z2[i], z3[i] = z3[i].copy(), z2[i].copy()

            if v1[1, i] < leftclip and v2[1, i] < leftclip and leftclip <= v3[1, i]:
                v1[:, i] = (v3[:, i] + (v1[:, i] - v3[:, i]) * (leftclip - v3[1, i]) / (v1[1, i] - v3[1, i])).copy()
                z1[i] = (z3[i] + (z1[i] - z3[i]) * (leftclip - v3[1, i]) / (v1[1, i] - v3[1, i])).copy()
                v2[:, i] = (v3[:, i] + (v2[:, i] - v3[:, i]) * (leftclip - v3[1, i]) / (v2[1, i] - v3[1, i])).copy()
                z2[i] = (z3[i] + (z2[i] - z3[i]) * (leftclip - v3[1, i]) / (v2[1, i] - v3[1, i])).copy()
                if n1 is not None:
                    n1[:, i] = (n3[:, i] + (n1[:, i] - n3[:, i]) * (leftclip - v3[1, i]) / (v1[1, i] - v3[1, i])).copy()
                    n2[:, i] = (n3[:, i] + (n2[:, i] - n3[:, i]) * (leftclip - v3[1, i]) / (v2[1, i] - v3[1, i])).copy()
            elif v1[1, i] < leftclip and leftclip <= v2[1, i] and leftclip <= v3[1, i]:
                tmpv1 = v2[:, i] + (v1[:, i] - v2[:, i]) * (leftclip - v2[1, i]) / (v1[1, i] - v2[1, i])
                tmpv2 = v3[:, i] + (v1[:, i] - v3[:, i]) * (leftclip - v3[1, i]) / (v1[1, i] - v3[1, i])
                tmpz1 = z2[i] + (z1[i] - z2[i]) * (leftclip - v2[1, i]) / (v1[1, i] - v2[1, i])
                tmpz2 = z3[i] + (z1[i] - z3[i]) * (leftclip - v3[1, i]) / (v1[1, i] - v3[1, i])
                v1[:, i] = tmpv1.copy()
                z1[i] = tmpz1.copy()
                v1 = np.concatenate([v1, tmpv1.copy().reshape(-1, 1)], axis=1)
                z1 = np.concatenate([z1, tmpz1.copy().reshape(1)])
                v2 = np.concatenate([v2, tmpv2.copy().reshape(-1, 1)], axis=1)
                z2 = np.concatenate([z2, tmpz2.copy().reshape(1)])
                v3 = np.concatenate([v3, v3[:, i].copy().reshape(-1, 1)], axis=1)
                z3 = np.concatenate([z3, z3[i].copy().reshape(1)])
                if c is not None:
                    tmpn1 = n2[:, i] + (n1[:, i] - n2[:, i]) * (leftclip - v2[1, i]) / (v1[1, i] - v2[1, i])
                    tmpn2 = n3[:, i] + (n1[:, i] - n3[:, i]) * (leftclip - v3[1, i]) / (v1[1, i] - v3[1, i])
                    n1[:, i] = tmpn1.copy()
                    n1 = np.concatenate([n1, tmpn1.copy().reshape(-1, 1)], axis=1)
                    n2 = np.concatenate([n2, tmpn2.copy().reshape(-1, 1)], axis=1)
                    n3 = np.concatenate([n3, n3[:, i].copy().reshape(-1, 1)], axis=1)
                    c = np.concatenate([c, c[:, i].copy().reshape(3, 1, 11)], axis=1)
                    wf = np.concatenate([wf, np.array([wf[i]])], axis=0)

        M, N = v1.shape
        for i in range(N):
            if v2[1, i] < v1[1, i]:
                v1[:, i], v2[:, i] = v2[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n2[:, i] = n2[:, i].copy(), n1[:, i].copy()
                z1[i], z2[i] = z2[i].copy(), z1[i].copy()
            if v3[1, i] < v1[1, i]:
                v1[:, i], v3[:, i] = v3[:, i].copy(), v1[:, i].copy()
                if n1 is not None:
                    n1[:, i], n3[:, i] = n3[:, i].copy(), n1[:, i].copy()
                z1[i], z3[i] = z3[i].copy(), z1[i].copy()
            if v3[1, i] < v2[1, i]:
                v2[:, i], v3[:, i] = v3[:, i].copy(), v2[:, i].copy()
                if n1 is not None:
                    n2[:, i], n3[:, i] = n3[:, i].copy(), n2[:, i].copy()
                z2[i], z3[i] = z3[i].copy(), z2[i].copy()

            if v1[1, i] <= rightclip and v2[1, i] <= rightclip and rightclip < v3[1, i]:
                tmpv1 = v1[:, i] + (v3[:, i] - v1[:, i]) * (rightclip - v1[1, i]) / (v3[1, i] - v1[1, i])
                tmpv2 = v2[:, i] + (v3[:, i] - v2[:, i]) * (rightclip - v2[1, i]) / (v3[1, i] - v2[1, i])
                tmpz1 = z1[i] + (z3[i] - z1[i]) * (rightclip - v1[1, i]) / (v3[1, i] - v1[1, i])
                tmpz2 = z2[i] + (z3[i] - z2[i]) * (rightclip - v2[1, i]) / (v3[1, i] - v2[1, i])
                v3[:, i] = tmpv1.copy()
                z3[i] = tmpz1.copy()
                v1 = np.concatenate([v1, tmpv1.copy().reshape(-1, 1)], axis=1)
                z1 = np.concatenate([z1, tmpz1.copy().reshape(1)])
                v2 = np.concatenate([v2, tmpv2.copy().reshape(-1, 1)], axis=1)
                z2 = np.concatenate([z2, tmpz2.copy().reshape(1)])
                v3 = np.concatenate([v3, v2[:, i].copy().reshape(-1, 1)], axis=1)
                z3 = np.concatenate([z3, z2[i].copy().reshape(1)])
                if c is not None:
                    tmpn1 = n1[:, i] + (n3[:, i] - n1[:, i]) * (rightclip - v1[1, i]) / (v3[1, i] - v1[1, i])
                    tmpn2 = n2[:, i] + (n3[:, i] - n2[:, i]) * (rightclip - v2[1, i]) / (v3[1, i] - v2[1, i])
                    n3[:, i] = tmpn1.copy()
                    n1 = np.concatenate([n1, tmpn1.copy().reshape(-1, 1)], axis=1)
                    n2 = np.concatenate([n2, tmpn2.copy().reshape(-1, 1)], axis=1)
                    n3 = np.concatenate([n3, n2[:, i].copy().reshape(-1, 1)], axis=1)
                    c = np.concatenate([c, c[:, i].copy().reshape(3, 1, 11)], axis=1)
                    wf = np.concatenate([wf, np.array([wf[i]])], axis=0)
            elif v1[1, i] <= rightclip and rightclip < v2[1, i] and rightclip < v3[1, i]:
                v2[:, i] = (v1[:, i] + (v2[:, i] - v1[:, i]) * (rightclip - v1[1, i]) / (v2[1, i] - v1[1, i])).copy()
                z2[i] = (z1[i] + (z2[i] - z1[i]) * (rightclip - v1[1, i]) / (v2[1, i] - v1[1, i])).copy()
                v3[:, i] = (v1[:, i] + (v3[:, i] - v1[:, i]) * (rightclip - v1[1, i]) / (v3[1, i] - v1[1, i])).copy()
                z3[i] = (z1[i] + (z2[i] - z1[i]) * (rightclip - v1[1, i]) / (v3[1, i] - v1[1, i])).copy()
                if n1 is not None:
                    n2[:, i] = (n1[:, i] + (n2[:, i] - n1[:, i]) * (rightclip - v1[1, i]) / (v2[1, i] - v1[1, i])).copy()
                    n3[:, i] = (n1[:, i] + (n3[:, i] - n1[:, i]) * (rightclip - v1[1, i]) / (v3[1, i] - v1[1, i])).copy()

        if n1 is not None:
            return v1, z1, v2, z2, v3, z3, n1, n2, n3, c, wf
        else:
            return v1, z1, v2, z2, v3, z3
