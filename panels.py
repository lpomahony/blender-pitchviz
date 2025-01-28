import bpy

class VIEW3D_PT_statcast_panel(bpy.types.Panel):
    bl_label = "Statcast Pitch Visualization"
    bl_idname = "VIEW3D_PT_statcast_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Statcast"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Import and Visualize Pitches")
        layout.operator("import_statcast.data", text="Select Statcast CSV")
        layout.operator("visualize_pitches.visualize", text="Visualize Pitches")

        layout.separator()
        layout.prop(scene, "group_by_at_bat")
        layout.prop(scene, "assign_pitch_materials")

        layout.separator()
        layout.operator("visualize_pitches.add_strike_zone", text="Create Strike Zone")

def register():
    bpy.utils.register_class(VIEW3D_PT_statcast_panel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_statcast_panel)