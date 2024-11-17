import bpy
from bpy.props import StringProperty

class SHOTDIAL_OT_AddImagePlane(bpy.types.Operator):
    bl_idname = "shotdial.add_image_plane"
    bl_label = "Add Image Plane"
    
    shot_name: StringProperty(name="Shot Name")

    def execute(self, context):
        rotation = context.scene.camera.rotation_euler
        bpy.ops.mesh.primitive_plane_add(size=1, align='VIEW', location=(0, 0, 0), rotation=rotation)
        plane = context.object
        prop_name = f"shot_visibility_{self.shot_name}"
        plane[prop_name] = 1
        cursor_loc = context.scene.cursor.location
        plane.location = cursor_loc
        plane.name = f"Image Plane {self.shot_name}"
        bpy.context.scene.transform_orientation_slots[0].type = 'VIEW'
        return {'FINISHED'}