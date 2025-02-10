import bpy

from .display_ot import MYADDON_OT_invisible_option

#パネル コライダー
class MYADDON_PT_invisible_option(bpy.types.Panel):
    bl_idname="MYADDON_PT_invisible_option"
    bl_label="非表示設定"
    bl_space_type="PROPERTIES"
    bl_region_type="WINDOW"
    bl_context="object"

    def draw(self,context):
        #パネルに項目を追加
        if "is_invisible" in context.object:

            #すでにプロパティがあれば、プロパティを表示
            self.layout.prop(context.object,'["is_invisible"]',text="is_Invisible")
        else:
            #プロパティが無ければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_invisible_option.bl_idname)

    
