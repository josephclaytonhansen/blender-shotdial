from os import path
import bpy

def append_node_group():
    try:
        script_dir=path.join(bpy.utils.script_path_user(), "addons", "shotdial")
        filepath = path.join(script_dir, "face_cull_shot_check.blend")
        node_group_name = "ShotCheck"

        if node_group_name not in bpy.data.node_groups:
            bpy.ops.wm.append(
                filepath=path.join(filepath, "NodeTree", node_group_name),
                directory=path.join(filepath, "NodeTree"),
                filename=node_group_name
            )

        global shotdial_node_group
        shotdial_node_group = bpy.data.node_groups.get(node_group_name)
        if not shotdial_node_group:
            print(f"Failed to append node group '{node_group_name}' from '{filepath}'")
    except Exception as e:
        print(f"Failed to append node group: {e}")