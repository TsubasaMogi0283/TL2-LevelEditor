import bpy
from .add_audio_information import MYADDON_OT_add_audio_information

#パネル
class OBJECT_PT_audio_information(bpy.types.Panel):
    bl_idname="OBJECT_PT_audio_information"
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
            self.layout.operator(MYADDON_OT_add_audio_information.bl_idname)