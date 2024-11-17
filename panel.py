import bpy

def update_shot_name(self, context):
    shot = bpy.context.scene.shotdial_shots.get(self.name)
    if shot:
        shot.name = self.name
        
def update_shot_color(self, context):
    shot = bpy.context.scene.shotdial_shots.get(self.name)
    mat = bpy.data.materials.get("ShotCheck")
    try:
        shot.color = self.color
        mat.diffuse_color = (*self.color, 1.0)
        bpy.data.grease_pencils["Annotations"].layers[shot.name].color = shot.color
    except Exception as e:
        print(f"Failed to update shot color: {e}")
        
class SHOTDIAL_PT_ShotPanel(bpy.types.Panel):
    bl_label = "ShotDial Panel"
    bl_idname = "SHOTDIAL_PT_shot_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ShotDial'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("shotdial.new_shot", text="New Shot")

        for shot in scene.shotdial_shots:
            box = layout.box()
            row = box.row()
            row.prop(shot, "name", text="")
            row.prop(shot, "color", text="Color")
            row = box.row()
            split = row.split(factor=0.8)
            col = split.column()
            op = col.operator("shotdial.set_active_camera", text="Preview")
            op.shot_name = shot.name
            col = split.column()
            col.operator("shotdial.remove_shot", text="", icon='TRASH').shot_name = shot.name
            box.separator()
            row = box.row()
            row.operator("shotdial.add_image_plane", text="Add Plane").shot_name = shot.name
            

def register():
    bpy.utils.register_class(SHOTDIAL_PT_ShotPanel)

def unregister():
    bpy.utils.unregister_class(SHOTDIAL_PT_ShotPanel)

if __name__ == "__main__":
    register()