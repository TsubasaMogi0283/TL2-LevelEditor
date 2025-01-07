import bpy
from .add_collider import MYADDON_OT_add_collider

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

