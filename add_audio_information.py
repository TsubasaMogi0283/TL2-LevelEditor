import bpy

#オーディオ
class MYADDON_OT_add_audio_information(bpy.types.Operator):
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
