import bpy


class MYADDON_OT_invisible_option(bpy.types.Operator):
    bl_idname="myddon.myaddon_ot_invisible_option"
    bl_label="非表示設定の追加"
    bl_description="['is_invisible']カスタムプロパティを追加します"
    bl_options={"REGISTER","UNDO"}


    def execute(self, context):
        context.object["is_invisible"]=True
        return {"FINISHED"}

