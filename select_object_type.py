import bpy

from .add_select_object_type import MYADDON_OT_add_select_object_type

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
            self.layout.operator(MYADDON_OT_add_select_object_type.bl_idname)