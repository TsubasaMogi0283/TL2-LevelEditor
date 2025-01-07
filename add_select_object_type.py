import bpy

#オペレータ カスタムプロパティ['object_type']追加
class MYADDON_OT_add_select_object_type(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_add_select_object_type"
    bl_label="オブジェクトのタイプを 選択"
    bl_description="['object_type']カスタムプロパティを追加します"
    bl_options={"REGISTER","UNDO"}

    #context...今選択中の
    def execute(self,context):
        #['file_name']カスタムプロパティを追加
        context.object["object_type"]="Stage"

        return {"FINISHED"}