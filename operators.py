import bpy
import csv
import os
from bpy.props import BoolProperty

class ImportStatcastDataOperator(bpy.types.Operator):
    bl_idname = "import_statcast.data"
    bl_label = "Import Statcast Data"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if not os.path.exists(self.filepath):
            self.report({"ERROR"}, "File not found")
            return {"CANCELLED"}

        with open(self.filepath, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            context.scene["statcast_data"] = [row for row in reader]

        self.report({"INFO"}, "Statcast Data Imported")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

class VisualizePitchesOperator(bpy.types.Operator):
    bl_idname = "visualize_pitches.visualize"
    bl_label = "Visualize Pitches"

    def execute(self, context):
        if "statcast_data" not in context.scene:
            self.report({'ERROR'}, "No Statcast data found. Please import a CSV first.")
            return {'CANCELLED'}

        from .visualize import create_pitch_curve, get_or_create_at_bat_collection, get_or_create_material
        data = context.scene["statcast_data"]

        group_by_at_bat = context.scene.group_by_at_bat
        assign_pitch_materials = context.scene.assign_pitch_materials

        for pitch_data in data:
            # Create the pitch curve (now a single object with integrated endpoint)
            curve_object = create_pitch_curve(pitch_data)

            # Handle grouping by at-bat
            if group_by_at_bat:
                at_bat_id = pitch_data.get("at_bat_number", "UnknownAtBat")
                at_bat_col = get_or_create_at_bat_collection(at_bat_id)
                
                if curve_object.name in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.unlink(curve_object)
                at_bat_col.objects.link(curve_object)

            # Handle materials
            if assign_pitch_materials:
                pitch_type = pitch_data.get("pitch_type", "UNK")
                mat = get_or_create_material(pitch_type)
                if not curve_object.data.materials:
                    curve_object.data.materials.append(mat)
                else:
                    curve_object.data.materials[0] = mat

        self.report({"INFO"}, f"Visualized {len(data)} pitches.")
        return {'FINISHED'}

class AddStrikeZoneOperator(bpy.types.Operator):
    bl_idname = "visualize_pitches.add_strike_zone"
    bl_label = "Add Strike Zone"

    def execute(self, context):
        from .visualize import create_strike_zone
        create_strike_zone()
        self.report({"INFO"}, "Strike Zone Created")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ImportStatcastDataOperator)
    bpy.utils.register_class(VisualizePitchesOperator)
    bpy.utils.register_class(AddStrikeZoneOperator)

    # Add our scene properties
    bpy.types.Scene.group_by_at_bat = BoolProperty(
        name="Group by At-Bat",
        description="Group pitches by at-bat in the outliner",
        default=False
    )
    bpy.types.Scene.assign_pitch_materials = BoolProperty(
        name="Assign Pitch Materials",
        description="Give each pitch a material based on pitch type",
        default=False
    )

def unregister():
    del bpy.types.Scene.group_by_at_bat
    del bpy.types.Scene.assign_pitch_materials

    bpy.utils.unregister_class(AddStrikeZoneOperator)
    bpy.utils.unregister_class(VisualizePitchesOperator)
    bpy.utils.unregister_class(ImportStatcastDataOperator)