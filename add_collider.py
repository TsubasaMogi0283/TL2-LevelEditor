import bpy
import mathutils

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
