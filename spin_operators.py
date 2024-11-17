import bpy

# Operator to cycle through cameras (forward)
class OBJECT_OT_Spin(bpy.types.Operator):
    """Move between camera views (forwards)"""
    bl_idname = "shotdial.spin"
    bl_label = "Move between camera views (forwards)"
    
    def execute(self, context):
        global camera_index
        cameras = [shot.name for shot in context.scene.shotdial_shots]

        if cameras:
            camera_index = (camera_index + 1) % len(cameras)
            context.scene.camera = bpy.data.objects.get(cameras[camera_index])
            bpy.ops.view3d.view_camera()
            self.report({'INFO'}, f"Switched to {cameras[camera_index]}")
        else:
            self.report({'ERROR'}, "No cameras found")
        return {'FINISHED'}

# Operator to cycle through cameras (backward)
class OBJECT_OT_DeSpin(bpy.types.Operator):
    """Move between camera views (backwards)"""
    bl_idname = "shotdial.despin"
    bl_label = "Move between camera views (backwards)"
    
    def execute(self, context):
        global camera_index
        cameras = [shot.name for shot in context.scene.shotdial_shots]

        if cameras:
            camera_index = (camera_index - 1) % len(cameras)
            context.scene.camera = bpy.data.objects.get(cameras[camera_index])
            bpy.ops.view3d.view_camera()
            self.report({'INFO'}, f"Switched to {cameras[camera_index]}")
        else:
            self.report({'ERROR'}, "No cameras found")
        return {'FINISHED'}