import bpy
from bpy.props import StringProperty

class SHOTDIAL_OT_SetActiveCamera(bpy.types.Operator):
    """Set the active camera for the selected shot"""
    bl_idname = "shotdial.set_active_camera"
    bl_label = "Set Active Camera"
    
    shot_name: StringProperty()

    def execute(self, context):
        shot = next((s for s in context.scene.shotdial_shots if s.name == self.shot_name), None)
        if shot.notes == "":
            bpy.data.scenes["Scene"].render.stamp_note_text = shot.name + " - " + shot.backgroundMotion + " - " + shot.scene_number
        else:
            bpy.data.scenes["Scene"].render.stamp_note_text = shot.name + " - " + shot.backgroundMotion + " - " + shot.scene_number + " (" + shot.notes + ")"
            
        bpy.data.scenes["Scene"].render.use_stamp_camera = True
        bpy.data.scenes["Scene"].render.use_stamp = True
        bpy.data.scenes["Scene"].render.use_stamp_filename = True
        bpy.data.scenes["Scene"].render.use_stamp_frame = True
        bpy.data.scenes["Scene"].render.use_stamp_frame_range = True
        bpy.data.scenes["Scene"].render.use_stamp_note = True
        bpy.data.scenes["Scene"].render.use_stamp_scene = False
        bpy.data.scenes["Scene"].render.use_stamp_date = False
        bpy.data.scenes["Scene"].render.use_stamp_time = False
        
        
        if shot:
            shot_check_mat = bpy.data.materials.get("ShotCheck")
            shot_check_mat.diffuse_color = (*shot.color, 1.0)

            gp = bpy.data.grease_pencils.get("Annotations")
            if gp:
                layer = gp.layers.get(shot.name)
                if layer:
                    for i, l in enumerate(gp.layers):
                        if l == layer:
                            gp.layers.active_index = i
                            break
                        
            for layer in gp.layers:
                layer.hide = False
                if layer.info != shot.name:
                    layer.hide = True
            
            cam_obj = shot.camera
            if cam_obj:
                context.scene.camera = cam_obj
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for space in area.spaces:
                            if space.type == 'VIEW_3D':
                                space.region_3d.view_perspective = 'CAMERA'
                                break
                
                # Show all mesh objects
                for obj in context.scene.objects:
                    if obj.type == 'MESH':
                        obj.hide_set(False)
                        obj.hide_viewport = False
                        obj.hide_render = False

                # Hide objects not visible in the shot
                prop_name = f"shot_visibility_{self.shot_name}"
                if not bpy.data.objects.get(prop_name):
                    obj.hide_set(True)
                    obj.hide_viewport = True
                    obj.hide_render = True
                for obj in context.scene.objects:
                    if obj.type == 'MESH':
                        if not obj.get(prop_name) == 1:
                            obj.hide_set(True)
                            obj.hide_viewport = True
                            obj.hide_render = True
                
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
                                    obj_info_node.inputs["Object"].default_value = shot.camera
                            except Exception as e:
                                self.report({'ERROR'}, f"Could not set camera on Object Info node: {e}")
                        except Exception as e:
                            self.report({'ERROR'}, f"Could not add ShotCheck modifier to object '{obj.name}': {e}")

                self.report({'INFO'}, f"Set '{shot.name}' as active camera")
            else:
                self.report({'ERROR'}, "Camera not found")
        else:
            self.report({'ERROR'}, "Shot not found")
        return {'FINISHED'}