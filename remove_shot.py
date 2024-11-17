import bpy
from bpy.props import StringProperty

class SHOTDIAL_OT_RemoveShot(bpy.types.Operator):
    """Remove a selected shot"""
    bl_idname = "shotdial.remove_shot"
    bl_label = "Remove Shot"
    
    shot_name: StringProperty()

    def execute(self, context):
        shot = next((s for s in context.scene.shotdial_shots if s.name == self.shot_name), None)
        if shot:
            gp = bpy.data.grease_pencils.get("Annotations")
            if gp:
                layer = gp.layers.get(shot.name)
                if layer:
                    gp.layers.remove(layer)

            context.scene.shotdial_shots.remove(context.scene.shotdial_shots.find(shot.name))
            self.report({'INFO'}, f"Shot '{shot.name}' removed")
        else:
            self.report({'ERROR'}, "Shot not found")
        return {'FINISHED'}