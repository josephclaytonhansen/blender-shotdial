bl_info = {
    "name": "ShotDial",
    "author": "Joseph Hansen",
    "version": (1, 3, 70),
    "blender": (3, 60, 13),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/josephclaytonhansen/blender-addons",
    "category": "3D View"
}

import bpy
from bpy.props import StringProperty, FloatVectorProperty, CollectionProperty, BoolProperty
from bpy.app.handlers import persistent
from .panel import SHOTDIAL_PT_ShotPanel
from .spin_operators import OBJECT_OT_Spin, OBJECT_OT_DeSpin
from .rename_shot import SHOTDIAL_OT_RenameShot
from .remove_shot import SHOTDIAL_OT_RemoveShot
from .append_node_group import append_node_group
from .new_shot import SHOTDIAL_OT_NewShot
from .set_active import SHOTDIAL_OT_SetActiveCamera
from .add_image_plane import SHOTDIAL_OT_AddImagePlane

def update_shot_name(self, context):
    shot = bpy.context.scene.shotdial_shots.get(self.name)
    if shot:
        shot.name = self.name
        
def update_scene_number(self, context):
    shot = bpy.context.scene.shotdial_shots.get(self.name)
    if shot:
        shot.sceneNumber = self.sceneNumber
        
def update_shot_time(self, context):
    shot = bpy.context.scene.shotdial_shots.get(self.name)
    if shot:
        shot.time = self.time

def update_shot_color(self, context):
    shot = bpy.context.scene.shotdial_shots.get(self.name)
    mat = bpy.data.materials.get("ShotCheck")
    try:
        shot.color = self.color
        mat.diffuse_color = (*self.color, 1.0)
        bpy.data.grease_pencils["Annotations"].layers[shot.name].color = shot.color
    except Exception as e:
        print(f"Failed to update shot color: {e}")
        
def update_shot_notes(self, context):
    shot = bpy.context.scene.shotdial_shots.get(self.name)
    if shot:
        shot.notes = self.notes
        
def update_shot_motion(self, context):
    shot = bpy.context.scene.shotdial_shots.get(self.name)
    if shot:
        shot.backgroundMotion = self.backgroundMotion
        
class ShotData(bpy.types.PropertyGroup):
    name: StringProperty(name="Name", default="Shot", update=update_shot_name)
    color: FloatVectorProperty(name="Color", subtype='COLOR', min=0, max=1, default=(1.0, 1.0, 1.0), update=update_shot_color)
    camera: bpy.props.PointerProperty(type=bpy.types.Object)
    time: bpy.props.EnumProperty(name="Time", items=[("DAY", "Day", ""), ("NIGHT", "Night", ""), ("DUSK", "Dusk", ""), ("DAWN", "Dawn", ""), ("MORNING", "Morning", ""), ("AFTERNOON", "Afternoon", ""), ("NOON", "Noon", ""), ("GOLDEN_HOUR", "Golden Hour", ""), ("MIDNIGHT", "Midnight", ""), ("SUNSET", "Sunset", ""), ("SUNRISE", "Sunrise", ""), ("EVENING", "Evening", ""), ("MIDNIGHT", "Midnight", "")], default="DAY", update=update_shot_time)
    sceneNumber: bpy.props.IntProperty(name="Scene #", default=0, update=update_scene_number, min=0)
    notes: bpy.props.StringProperty(name="Notes", default="", update=update_shot_notes)
    backgroundMotion: bpy.props.EnumProperty(name="Background Motion", items=[("STATIC", "Static", ""), ("TRACKING", "Tracking", ""), ("SHAKE", "Shake", ""), ("PAN_LEFT", "Pan Left", ""), ("PAN_RIGHT", "Pan Right", ""), ("PAN_UP", "Pan Up", ""), ("PAN_DOWN", "Pan Down", ""), ("ZOOM_IN", "Zoom In", ""), ("ZOOM_OUT", "Zoom Out", ""), ("DOLLY_IN", "Dolly In", ""), ("DOLLY_OUT", "Dolly Out", ""),  ("TILT_UP", "Tilt Up", ""), ("TILT_DOWN", "Tilt Down", ""), ("ROLL_LEFT", "Roll Left", ""), ("ROLL_RIGHT", "Roll Right", "")], default="STATIC", update=update_shot_motion)

camera_index = 0
addon_keymaps = []
shotdial_node_group = None

@persistent
def load_handler(dummy):
    append_node_group()
    try:
        bpy.ops.gpencil.annotation_add()
    except Exception as e:
        print(f"Failed to add annotation layer: {e}")

classes = [
    ShotData,
    SHOTDIAL_OT_NewShot,
    SHOTDIAL_PT_ShotPanel,
    SHOTDIAL_OT_SetActiveCamera,
    OBJECT_OT_Spin,
    OBJECT_OT_DeSpin,
    SHOTDIAL_OT_RenameShot,
    SHOTDIAL_OT_RemoveShot,
    SHOTDIAL_OT_AddImagePlane
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.shotdial_shots = CollectionProperty(type=ShotData)
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.shotdial_shots
    bpy.app.handlers.load_post.remove(load_handler)


if __name__ == "__main__":
    register()