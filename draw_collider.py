import bpy
import gpu
import gpu_extras.batch
import mathutils

#コライダーの描画
class DrawCollider:

    #描画ハンドル
    handle=None
    
    # 3Dビューに登録する描画関数
    def draw():
        
        # 頂点データ
        vertices = {"pos": []}
        # インデックスデータ
        indices = []
        
        # 基本の立方体の頂点オフセット（立方体の中心からの相対位置）
        offsets = [
            [-0.5, -0.5, -0.5],  # 左下前
            [+0.5, -0.5, -0.5],  # 右下前
            [-0.5, +0.5, -0.5],  # 左上前
            [+0.5, +0.5, -0.5],  # 右上前
            [-0.5, -0.5, +0.5],  # 左下奥
            [+0.5, -0.5, +0.5],  # 右下奥
            [-0.5, +0.5, +0.5],  # 左上奥
            [+0.5, +0.5, +0.5],  # 右上奥
        ]

        # 現在シーンのオブジェクトリストを走査
        for object in bpy.context.scene.objects:
            # コライダープロパティが無ければ、描画をスキップ
            if not ("collider_center" in object and "collider_size" in object):
                continue

            # オブジェクトのコライダー中心とサイズを取得
            collider_center = mathutils.Vector(object["collider_center"])
            collider_size = mathutils.Vector(object["collider_size"])

            # スケールを無視した位置と回転のみの行列を作成
            rotation_matrix = object.matrix_world.to_3x3().normalized().to_4x4()
            translation_matrix = mathutils.Matrix.Translation(object.location)
            transform_matrix = translation_matrix @ rotation_matrix  # 位置と回転のみの行列

            # 追加前の頂点数
            start = len(vertices["pos"])

            # 立方体の8頂点分を回す
            for offset in offsets:
                # コライダーサイズとオフセットに基づく頂点位置
                pos = collider_center + mathutils.Vector(
                    (offset[0] * collider_size[0],
                     offset[1] * collider_size[1],
                     offset[2] * collider_size[2])
                )
                
                # スケール無視したワールド座標に変換
                pos = transform_matrix @ pos

                # 頂点データリストに座標を追加
                vertices['pos'].append(pos)

            # 前面を構成する辺の頂点インデックスデータ
            indices.append([start + 0, start + 1])
            indices.append([start + 2, start + 3])
            indices.append([start + 0, start + 2])
            indices.append([start + 1, start + 3])
            # 奥面を構成する辺の頂点インデックス
            indices.append([start + 4, start + 5])
            indices.append([start + 6, start + 7])
            indices.append([start + 4, start + 6])
            indices.append([start + 5, start + 7])
            # 前と奥を繋ぐ辺の頂点インデックス
            indices.append([start + 0, start + 4])
            indices.append([start + 1, start + 5])
            indices.append([start + 2, start + 6])
            indices.append([start + 3, start + 7])

        # シェーダーを取得して描画を設定
        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        batch = gpu_extras.batch.batch_for_shader(shader, "LINES", vertices, indices=indices)

        # シェーダのパラメータ設定
        color = [0.5, 1.0, 1.0, 1.0]
        shader.bind()
        shader.uniform_float("color", color)
        # 描画
        batch.draw(shader)
