class GraphicsPipeline:
    """Graphics Pipeline"""
    # https://en.wikipedia.org/wiki/Graphics_pipeline
    # https://ja.wikipedia.org/wiki/グラフィックスパイプライン
    # https://en.wikipedia.org/wiki/Shading
    # https://en.wikipedia.org/wiki/Phong_shading
    # https://en.wikipedia.org/wiki/Rendering_(computer_graphics)

    @staticmethod
    def create_shadow_map(lightpos, lightrot, ortho, v1, v2, v3, tn, shadow_map_size=2048):
        R = lightrot.matrix
        T = -np.matmul(lightrot.matrix, lightpos.reshape(3, 1))

        c_uv = shadow_map_size // 2
        focal = c_uv

        shadow_map = Layer(shadow_map_size, shadow_map_size, focal, c_uv, c_uv, "shadow map", layer_type=2)
        shadow_map.save_pos_rot(lightpos, lightrot)

        if v1.size == 0:
            return shadow_map
        else:
            v1 = ShaderVertex.transform_world_to_camera(R, T, v1)
            v2 = ShaderVertex.transform_world_to_camera(R, T, v2)
            v3 = ShaderVertex.transform_world_to_camera(R, T, v3)
            tn = ShaderVertex.transform_world_to_camera(R, T, n=tn)

            v1, v2, v3 = ShaderGeometry.frontface_culling(v1, v2, v3, tn)
            v1, v2, v3 = ShaderGeometry.depth_clip(v1, v2, v3, Settings.LIGHT_NEARCLIP, Settings.LIGHT_FARCLIP)

            v1, z1 = ShaderVertex.transform_camera_to_canvas(focal, c_uv, c_uv, v1, ortho)
            v2, z2 = ShaderVertex.transform_camera_to_canvas(focal, c_uv, c_uv, v2, ortho)
            v3, z3 = ShaderVertex.transform_camera_to_canvas(focal, c_uv, c_uv, v3, ortho)

            v1, z1, v2, z2, v3, z3 = ShaderGeometry.side_clip(v1, z1, v2, z2, v3, z3, c_uv, c_uv)

            v1 = v1.astype('i8')
            v2 = v2.astype('i8')
            v3 = v3.astype('i8')

            for i in range(z1.size):
                Triangle2D.filled_triangle(shadow_map, v1[0, i], v1[1, i], v2[0, i], v2[1, i], v3[0, i], v3[1, i], z0=z1[i], z1=z2[i], z2=z3[i])

            return shadow_map

    @staticmethod
    def main_pipeline(canvas, campos, camrot, ortho, lights, shadows, v1, n1, v2, n2, v3, n3, tn, c, wf):
        R = camrot.matrix
        T = -np.matmul(camrot.matrix, campos.reshape(3, 1))

        canvas.main_layer.save_pos_rot(campos, camrot)

        c = c.reshape((3, -1, 11))

        v1 = ShaderVertex.transform_world_to_camera(R, T, v1)
        v2 = ShaderVertex.transform_world_to_camera(R, T, v2)
        v3 = ShaderVertex.transform_world_to_camera(R, T, v3)
        tn = ShaderVertex.transform_world_to_camera(R, T, n=tn)
        n1 = n1.T
        n2 = n2.T
        n3 = n3.T

        v1, v2, v3, tn, n1, n2, n3, c, wf = ShaderGeometry.backface_culling(v1, v2, v3, tn, n1, n2, n3, c, wf)
        v1, v2, v3, tn, n1, n2, n3, c, wf = ShaderGeometry.depth_clip(v1, v2, v3, Settings.CAMERA_NEARCLIP, Settings.CAMERA_FARCLIP, tn, n1, n2, n3, c, wf)

        v1, z1 = ShaderVertex.transform_camera_to_canvas(Settings.FOCAL, Settings.C_U, Settings.C_V, v1, ortho)
        v2, z2 = ShaderVertex.transform_camera_to_canvas(Settings.FOCAL, Settings.C_U, Settings.C_V, v2, ortho)
        v3, z3 = ShaderVertex.transform_camera_to_canvas(Settings.FOCAL, Settings.C_U, Settings.C_V, v3, ortho)

        v1, z1, v2, z2, v3, z3, n1, n2, n3, c, wf = ShaderGeometry.side_clip(v1, z1, v2, z2, v3, z3, Settings.C_U, Settings.C_V, n1, n2, n3, c, wf)

        v1 = v1.astype('i8')
        v2 = v2.astype('i8')
        v3 = v3.astype('i8')

        for i in range(z1.size):
            if wf[i]:
                Triangle2D.triangle(canvas.main_layer, v1[0, i], v1[1, i], v2[0, i], v2[1, i], v3[0, i], v3[1, i], c[0, i], c[1, i], c[2, i], z1[i], z2[i], z3[i], n1[:, i], n2[:, i], n3[:, i], lights, shadows)
            else:
                Triangle2D.filled_triangle(canvas.main_layer, v1[0, i], v1[1, i], v2[0, i], v2[1, i], v3[0, i], v3[1, i], c[0, i], c[1, i], c[2, i], z1[i], z2[i], z3[i], n1[:, i], n2[:, i], n3[:, i], lights, shadows)

    @staticmethod
    def run(canvas, camera, world):
        v1 = np.array([[0, 0, 0]])
        n1 = np.array([[0, 0, 0]])
        v2 = np.array([[0, 0, 0]])
        n2 = np.array([[0, 0, 0]])
        v3 = np.array([[0, 0, 0]])
        n3 = np.array([[0, 0, 0]])
        tn = np.array([[0, 0, 0]])
        tm = Material.clear_material.reshape(1, -1)
        wf = np.array([False])
        sh = np.array([False])
        for world_object in world.objects:
            v1 = np.concatenate([v1, np.matmul(world_object.rot.matrix, world_object.v[:, :, 0].T).T + world_object.pos], axis=0)
            n1 = np.concatenate([n1, np.matmul(world_object.rot.matrix, world_object.vn[:, :, 0].T).T], axis=0)
            v2 = np.concatenate([v2, np.matmul(world_object.rot.matrix, world_object.v[:, :, 1].T).T + world_object.pos], axis=0)
            n2 = np.concatenate([n2, np.matmul(world_object.rot.matrix, world_object.vn[:, :, 1].T).T], axis=0)
            v3 = np.concatenate([v3, np.matmul(world_object.rot.matrix, world_object.v[:, :, 2].T).T + world_object.pos], axis=0)
            n3 = np.concatenate([n3, np.matmul(world_object.rot.matrix, world_object.vn[:, :, 2].T).T], axis=0)
            tn = np.concatenate([tn, np.matmul(world_object.rot.matrix, world_object.tn.reshape(-1, 3).T).T], axis=0)
            tm = np.concatenate([tm, world_object.tm], axis=0)
            wf = np.concatenate([wf, np.tile(np.array([world_object.wire_frame]), (world_object.v.shape[0]))], axis=0)
            sh = np.concatenate([sh, np.tile(np.array([world_object.enable_shadow]), (world_object.v.shape[0]))], axis=0)
        v1 = v1[1:, :]
        n1 = n1[1:, :]
        v2 = v2[1:, :]
        n2 = n2[1:, :]
        v3 = v3[1:, :]
        n3 = n3[1:, :]
        tn = tn[1:, :]
        tm = tm[1:, :]
        wf = wf[1:]
        sh = sh[1:]

        time_ini = time.perf_counter()

        shadows = []
        for light_id in range(len(world.lights)):
            light = world.lights[light_id]
            if light.light_type == 0:
                shadows.append("")
            else:
                shadows.append(GraphicsPipeline.create_shadow_map(light.pos, light.rot, light.light_type==2, v1[np.invert(wf) & sh, :], v2[np.invert(wf) & sh, :], v3[np.invert(wf) & sh, :], tn[np.invert(wf) & sh, :]))

        c = np.tile(tm, (3, 1, 1))

        time_sha = time.perf_counter()

        GraphicsPipeline.main_pipeline(canvas, camera.pos, camera.rot, camera.ortho, world.lights, shadows, v1, n1, v2, n2, v3, n3, tn, c, wf)

        time_end = time.perf_counter()

        return shadows, time_ini, time_sha, time_end
