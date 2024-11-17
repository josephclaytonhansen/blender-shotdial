import bpy

class SHOTDIAL_OT_RenameShot(bpy.types.Operator):
    """Rename a selected shot and its associated camera"""
    bl_idname = "shotdial.rename_shot"
    bl_label = "Rename Shot"

    new_name: bpy.props.StringProperty()

    def execute(self, context):
        shot = next((s for s in context.scene.shotdial_shots if s.name == self.new_name), None)
        if shot:
            shot.name = self.new_name
            if shot.camera:
                shot.camera.name = self.new_name
                self.report({'INFO'}, f"Shot and camera renamed to '{self.new_name}'")
            else:
                self.report({'ERROR'}, "Associated camera not found")
        else:
            self.report({'ERROR'}, "Shot not found")
        return {'FINISHED'}