import bpy
import random
import mathutils
from bpy_extras.object_utils import world_to_camera_view

class SHOTDIAL_OT_NewShot(bpy.types.Operator):
    """Add a new shot"""
    bl_idname = "shotdial.new_shot"
    bl_label = "New Shot"

    def execute(self, context):
        if context.scene.camera:
            cam_obj = context.scene.camera
        else:
            cam_data = bpy.data.cameras.new(name="Camera")
            cam_obj = bpy.data.objects.new(name="Camera", object_data=cam_data)
            context.scene.collection.objects.link(cam_obj)
            context.scene.camera = cam_obj

        shot_name = f"Shot {len(context.scene.shotdial_shots) + 1}"
        shot_color = (random.random(), random.random(), random.random())
        new_shot = context.scene.shotdial_shots.add()
        new_shot.name = shot_name
        new_shot.color = shot_color
        new_shot.camera = cam_obj
        cam_obj.name = shot_name

        shot_check_mat = bpy.data.materials.get("ShotCheck") or bpy.data.materials.new("ShotCheck")
        shot_check_mat.use_nodes = True

        shot_check_mat.diffuse_color = (*shot_color, 1.0)

        scene = context.scene
        cam = scene.camera
        
        bpy.ops.gpencil.layer_annotation_add()
        bpy.data.grease_pencils["Annotations"].layers["Note"].info = new_shot.name
        bpy.data.grease_pencils["Annotations"].layers[new_shot.name].color = new_shot.color

        for layer in bpy.data.grease_pencils["Annotations"].layers:
            layer.hide = False
            if layer.info != new_shot.name:
                layer.hide = True

        def is_in_camera_view(obj, cam):
            for vert in obj.bound_box:
                co = obj.matrix_world @ mathutils.Vector(vert)
                co_cam = world_to_camera_view(scene, cam, co)
                if 0.0 <= co_cam.x <= 1.0 and 0.0 <= co_cam.y <= 1.0 and co_cam.z >= 0.0:
                    return True
            return False

        for obj in context.scene.objects:
            if obj.type != 'MESH' or obj.hide_render:
                continue
            else:
                if not obj.modifiers.get("ShotCheck"):
                    modifier = obj.modifiers.new(name="ShotCheck", type='NODES')
                else:
                    modifier = obj.modifiers["ShotCheck"]
                    try:
                        modifier.node_group = bpy.data.node_groups.get("ShotCheck")
                        try:
                            obj_info_node = modifier.node_group.nodes.get("Object Info")
                            if obj_info_node:
                                obj_info_node.inputs["Object"].default_value = new_shot.camera
                        except Exception as e:
                            self.report({'ERROR'}, f"Could not set camera on Object Info node: {e}")
                    except Exception as e:
                        self.report({'ERROR'}, f"Could not add ShotCheck modifier to object '{obj.name}': {e}")

                prop_name = f"shot_visibility_{shot_name}"
                obj[prop_name] = 1 if is_in_camera_view(obj, cam) else 0
                obj.hide_set(not obj[prop_name])
                obj.hide_viewport = not obj[prop_name]

        self.report({'INFO'}, f"Shot '{shot_name}' created")
        return {'FINISHED'}