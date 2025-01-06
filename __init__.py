import bpy
import math
import bpy_extras
import gpu
import gpu_extras.batch
import copy
import mathutils
import json


from bpy.props import (EnumProperty,BoolProperty)
#同じlevel_editorフォルダに入っているpyファイルからインポートするよ
from .stretch_vertex import MYADDON_OT_stretch_vertex
from .create_ico_sphere import MYDDON_OT_create_ico_sphere
from .export_scene import MYADDON_OT_export_scene


#Blenderに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Tsubasa Mogi",
    "version": (1,0),
    "blender": (4,1,0),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "Object"
}




#Pythonは変数などを宣言するときに型を書く必要はないよ
#ex)string="Text"
#C++だとこうだね
#std::string string="Text"

#メニュー項目描画
def draw_menu_manual(self,context):
    #self:呼び出し元のクラスインスタンス。C++でいう thisポインタ
    #context:カーソルを合わせた時のポップアップのカスタマイズなどに使用
    
    #トップバーの「エディターメニュー」に項目(オペレータ)を追加
    self.layout.operator("wm.url_open_preset",text="Manual",icon="HELP")
    #区切り線
    self.layout.separator()
    self.layout.operator("wm.url_open_preset",text="Manual2",icon="HELP")
    
    





#パネル ファイル名
class OBJECT_PT_file_name(bpy.types.Panel):
    """オブジェクトのファイルネームパネル"""
    bl_idname="OBJECT_PT_file_name"
    bl_label="モデルのファイル名"
    bl_space_type="PROPERTIES"
    bl_region_type="WINDOW"
    bl_context="object"

    #サブメニューの描画
    def draw(self,context):
        #パネルに項目を追加
        if "file_name" in context.object:
            #すでにプロパティがあれば、プロパティを表示
            self.layout.prop(context.object,'["file_name"]',text=self.bl_label)
        else:
            #プロパティが無ければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)

#オペレータ カスタムプロパティ['file_name']追加
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_add_filename"
    bl_label="ファイル名を追加"
    bl_description="['file_name']カスタムプロパティを追加します"
    bl_options={"REGISTER","UNDO"}

    #context...今選択中の
    def execute(self,context):
        #['file_name']カスタムプロパティを追加
        context.object["file_name"]=""

        return {"FINISHED"}

#オペレータ カスタムプロパティ['object_type']追加
class MYADDON_OT_select_object_type(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_select_object_type"
    bl_label="オブジェクトのタイプを 選択"
    bl_description="['object_type']カスタムプロパティを追加します"
    bl_options={"REGISTER","UNDO"}

    #context...今選択中の
    def execute(self,context):
        #['file_name']カスタムプロパティを追加
        context.object["object_type"]="Stage"

        return {"FINISHED"}

#オブジェクトの種類を選択
class OBJECT_OT_select_object_type(bpy.types.Panel):
    bl_idname="OBJECT_PT_object_type"
    bl_label="ObjectType"
    bl_space_type="PROPERTIES"
    bl_region_type="WINDOW"
    bl_context="object"

    #サブメニューの描画
    def draw(self,context):
        #パネルに項目を追加
        if "object_type" in context.object:
            #すでにプロパティがあれば、プロパティを表示
            self.layout.prop(context.scene, "objectTypeSelection", text="種類")
        else:
            #プロパティが無ければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_select_object_type.bl_idname)

#region Collider

#オペレータ カスタムプロパティ['collider']追加
class MYADDON_OT_add_collider(bpy.types.Operator):
    bl_idname="myddon.myaddon_ot_add_collider"
    bl_label="コライダー 追加"
    bl_description="['collider']カスタムプロパティを追加します"
    bl_options={"REGISTER","UNDO"}


    def execute(self,context):
        
        #['collider']カスタムプロパティを追加
        context.object["collider_type"]="BOX"
        context.object["collider_center"]=mathutils.Vector((0,0,0))
        context.object["collider_size"]=mathutils.Vector((1,1,1))

        return {"FINISHED"}

#パネル コライダー
class OBJECT_PT_collider(bpy.types.Panel):
    bl_idname="OBJECT_PT_collider"
    bl_label="Collider"
    bl_space_type="PROPERTIES"
    bl_region_type="WINDOW"
    bl_context="object"

    def draw(self,context):
        #パネルに項目を追加
        if "collider_type" in context.object:

            #すでにプロパティがあれば、プロパティを表示
            self.layout.prop(context.object,'["collider_type"]',text="Type")
            self.layout.prop(context.object,'["collider_center"]',text="Center")
            self.layout.prop(context.object,'["collider_size"]',text="Size")
        else:
            #プロパティが無ければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_collider.bl_idname)

#コライダー描画
class DrawCollider:

    #描画ハンドル
    handle=None
    
    # 3Dビューに登録する描画関数
    def draw_collider():
        
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

#endregion

#オーディオ
class MYADDON_OT_add_audio_filename(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_add_audio_filename"
    bl_label="オーディオのファイル名を追加"
    bl_description="['audio_file_name']カスタムプロパティを追加します"
    bl_options={"REGISTER","UNDO"}

    #context...今選択中の
    def execute(self,context):
        #['file_name']カスタムプロパティを追加
        context.object["audio_file_name"]=""
        context.object["audio_type"]="BGM"
        context.object["audio_loop"]=True
        context.object["audio_on_area"]=True
        
        return {"FINISHED"}

#パネル
class AUDIO_PT_fileName(bpy.types.Panel):
    bl_idname="OBJECT_PT_audio"
    bl_label="Audio"
    bl_space_type="PROPERTIES"
    bl_region_type="WINDOW"
    bl_context="object"

    #サブメニューの描画
    def draw(self,context):
        #パネルに項目を追加
        if "audio_file_name" in context.object:
            #すでにプロパティがあれば、プロパティを表示
            self.layout.prop(context.object,'["audio_file_name"]',text="ファイル名")
            self.layout.prop(context.scene, "cm_prop_enum", text="種類")
            self.layout.prop(context.object, '["audio_loop"]', text="ループ")
            self.layout.prop(context.object, '["audio_on_area"]', text="エリア上")
        else:
            #プロパティが無ければ、プロパティ追加ボタンを表示
            #機能は同じでも違うものにしないと共有されてしまうことに気づいた
            self.layout.operator(MYADDON_OT_add_audio_filename.bl_idname)
        
#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #クラスの書き方はだいたいC++と同じだね
    #()内に継承するものをいれる

    #Blenderがクラスを識別するための固有の文字列
    bl_idname="TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label="MyMenyu"
    #著者表示用の文字列
    bl_description="拡張メニュー by"+bl_info["author"]

    #サブメニューの描画
    def draw(self,context):
        #トップバーの「エディターメニュー」に項目(オペレータ)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,text=MYADDON_OT_stretch_vertex.bl_label)
        self.layout.operator(MYDDON_OT_create_ico_sphere.bl_idname,text=MYDDON_OT_create_ico_sphere.bl_label)
        self.layout.operator(MYADDON_OT_export_scene.bl_idname,text=MYADDON_OT_export_scene.bl_label)
        

    #既存のメニューにサブメニューを追加
    def submenu(self,context):
        #ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

#Blenderに登録するクラスリスト
#順番は関係無いよ
classes=(
    MYADDON_OT_stretch_vertex,
    MYDDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
    AUDIO_PT_fileName,
    MYADDON_OT_add_audio_filename,
    OBJECT_OT_select_object_type,
    MYADDON_OT_select_object_type,
    )




# プロパティの初期化
def init_props():
    scene = bpy.types.Scene
    #オーディオ
    scene.cm_prop_enum = EnumProperty(
        name="種類",
        description="オ－ディオの種類を選択",
        items=[
            ('ITEM_1', "BGM", "BGM"),
            ('ITEM_2', "Action", "Action"),
        ],
        default='ITEM_1',
        update=update_audio_type
    )
    scene.audio_loop = BoolProperty(
        name="ループ",
        description="ループの設定",
        default=True,
        update=update_audio_loop
    )

    scene.audio_on_area = BoolProperty(
        name="エリア",
        description="エリア上かどうかの設定",
        default=True,
        update=update_audio_on_area
    )

    #オブジェクト
    scene.objectTypeSelection = EnumProperty(
        name="オブジェクトの種類",
        description="オブジェクトの種類を選択",
        items=[
            ('ITEM_1', "Stage", "Stage"),
            ('ITEM_2', "Audio", "Audio"),
        ],
        default='ITEM_1',
        update=update_object_type
    )

def update_audio_type(self, context):
    # 選択したEnumの値をcontext.object["audio_type"]に反映
    enum_value = context.scene.cm_prop_enum
    if enum_value == 'ITEM_1':
        context.object["audio_type"] = "BGM"
    elif enum_value == 'ITEM_2':
        context.object["audio_type"] = "Action"

def update_audio_loop(self,context):
    if context.scene.audio_loop:
        context.object["audio_loop"] = True
    else:
        context.object["audio_loop"] = False
      
def update_audio_on_area(self,context):
    if context.scene.audio_on_area:
        context.object["audio_on_area"] = True
    else:
        context.object["audio_on_area"] = False
 
def update_object_type(self, context):
    # 選択したEnumの値をcontext.object["object_type"]に反映
    enum_value = context.scene.objectTypeSelection
    if enum_value == 'ITEM_1':
        context.object["object_type"] = "Stage"
    elif enum_value == 'ITEM_2':
        context.object["object_type"] = "Audio"


# プロパティを削除
def clear_props():
    scene = bpy.types.Scene
    del scene.cm_prop_enum
    del scene.objectTypeSelection
    if hasattr(scene, "audio_loop"):
        del scene.audio_loop
    if hasattr(scene, "audio_on_area"):
        del scene.audio_on_area

#アドオン有効化時コールバック
def register() :
    #Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)
    init_props()
    #メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    #3Dビューに描画関数を追加
    DrawCollider.handle=bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider,(),"WINDOW","POST_VIEW")
    print("レベルエディタが有効化されました")


#アドオン無効化時コールバック
def unregister() :
    #メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    #3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle,"WINDOW")
    clear_props()
    #Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("レベルエディタが無効化されました")

