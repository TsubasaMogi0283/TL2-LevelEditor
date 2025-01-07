import bpy

from . import bl_info
from .stretch_vertex import MYADDON_OT_stretch_vertex
from .create_ico_sphere import MYDDON_OT_create_ico_sphere
from .export_scene import MYADDON_OT_export_scene



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
