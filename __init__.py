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

#ファイル名の追加
from .add_filename import MYADDON_OT_add_filename
from .filename import OBJECT_PT_filename

#オブジェクトタイプの設定
from .add_select_object_type import MYADDON_OT_add_select_object_type
from .select_object_type import OBJECT_OT_select_object_type

#オーディオ
from .add_audio_information import MYADDON_OT_add_audio_information
from .audio_information import OBJECT_PT_audio_information
#コライダー
from .add_collider import MYADDON_OT_add_collider
from .draw_collider import DrawCollider
from .collider import OBJECT_PT_collider


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

#トップバー
#bl_infoを使いたいのでここでfrom,importを使う
from .topbar_my_menu import TOPBAR_MT_my_menu



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


#Blenderに登録するクラスリスト
#順番は関係無いよ
classes=(
    MYADDON_OT_stretch_vertex,
    MYDDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_filename,
    OBJECT_PT_filename,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
    OBJECT_PT_audio_information,
    MYADDON_OT_add_audio_information,
    OBJECT_OT_select_object_type,
    MYADDON_OT_add_select_object_type,
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
    DrawCollider.handle=bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw,(),"WINDOW","POST_VIEW")
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

