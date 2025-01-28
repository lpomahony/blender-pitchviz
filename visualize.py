import bpy
import math

def feet_to_meters(feet):
    return feet * 0.3048

def create_strike_zone():
    """
    Creates a strike zone using Statcast's universal dimensions.
    Width: 17 inches (±8.5 inches from center)
    Height: Typically 1.5 to 3.5 feet (but can vary by batter)
    """
    width = feet_to_meters(17/12)  # 17 inches to feet, then to meters
    height = feet_to_meters(2.0)   # ~2 feet tall (1.5 to 3.5 range)
    thickness = feet_to_meters(0.01)
    
    # Position center of strike zone at origin (where plate_x/z are measured)
    center_z = feet_to_meters(2.5)  # Center height
    
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(0, 0, center_z)
    )
    
    zone_obj = bpy.context.active_object
    zone_obj.name = "StrikeZone"
    zone_obj.scale = (width/2, thickness, height/2)
    
    # Add wireframe for visibility
    wire_mod = zone_obj.modifiers.new(name="Wireframe", type='WIREFRAME')
    wire_mod.thickness = 0.001
    
    return zone_obj

def create_pitch_curve(pitch_data, num_points=20):
    """
    Creates a 3D curve representing pitch trajectory using Statcast data.
    Includes both the trajectory and the "endpoint" as part of the same curve.
    """
    # Extract raw values (in feet)
    x0 = float(pitch_data.get("release_pos_x", 0.0))
    y0 = float(pitch_data.get("release_pos_y", 50.0))
    z0 = float(pitch_data.get("release_pos_z", 6.0))
    
    vx0 = float(pitch_data.get("vx0", 0.0))
    vy0 = float(pitch_data.get("vy0", 0.0))
    vz0 = float(pitch_data.get("vz0", 0.0))
    
    ax = float(pitch_data.get("ax", 0.0))
    ay = float(pitch_data.get("ay", 0.0))
    az = float(pitch_data.get("az", 0.0))
    
    # Calculate time to plate
    T = abs(y0 / vy0) if vy0 != 0 else 0.5
    
    # Generate points along trajectory
    times = [i * T / (num_points - 1) for i in range(num_points)]
    coords = []
    
    for t in times:
        x_t = x0 + vx0*t + 0.5*ax*(t**2)
        y_t = y0 + vy0*t + 0.5*ay*(t**2)
        z_t = z0 + vz0*t + 0.5*az*(t**2)
        coords.append((
            feet_to_meters(x_t),
            feet_to_meters(y_t),
            feet_to_meters(z_t)
        ))
    
    # Create curve
    curve_data = bpy.data.curves.new("PitchTrajectory", type="CURVE")
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 12
    curve_data.bevel_depth = feet_to_meters(0.12)  # Baseball radius
    
    # Create main trajectory
    spline = curve_data.splines.new('NURBS')
    spline.points.add(len(coords) - 1)
    
    for i, coord in enumerate(coords):
        x, y, z = coord
        spline.points[i].co = (x, y, z, 1)
    
    # Create endpoint (using a small sphere-like curve)
    end_x, end_y, end_z = coords[-1]
    endpoint = curve_data.splines.new('NURBS')
    endpoint.points.add(7)  # 8 points for a simple sphere approximation
    
    radius = feet_to_meters(0.12)  # Baseball radius
    for i, angle in enumerate(range(0, 360, 45)):
        rad = math.radians(angle)
        x = end_x + radius * math.cos(rad)
        y = end_y
        z = end_z + radius * math.sin(rad)
        endpoint.points[i].co = (x, y, z, 1)
    
    endpoint.use_cyclic_u = True  # Close the circle
    
    # Create and link object
    curve_obj = bpy.data.objects.new("Pitch", curve_data)
    bpy.context.scene.collection.objects.link(curve_obj)
    
    return curve_obj

def get_or_create_at_bat_collection(at_bat_id):
    """Create or get collection for grouping pitches by at-bat"""
    col_name = f"AtBat_{at_bat_id}"
    existing = bpy.data.collections.get(col_name)
    if existing:
        return existing
    
    new_col = bpy.data.collections.new(col_name)
    bpy.context.scene.collection.children.link(new_col)
    return new_col

def get_or_create_material(pitch_type):
    """Create or get material for pitch visualization"""
    mat_name = f"Pitch_{pitch_type}"
    mat = bpy.data.materials.get(mat_name)
    
    if mat is None:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        
        # Colors matching Baseball Savant
        color_map = {
            "FF": (0.95, 0.1, 0.1, 1.0),   # Four-seam: Red
            "SI": (0.95, 0.5, 0.1, 1.0),   # Sinker: Orange
            "CU": (0.1, 0.1, 0.95, 1.0),   # Curveball: Blue
            "SL": (0.8, 0.8, 0.0, 1.0),    # Slider: Yellow
            "CH": (0.0, 0.8, 0.0, 1.0),    # Changeup: Green
            "FC": (0.8, 0.1, 0.8, 1.0),    # Cutter: Purple
        }
        
        base_color = color_map.get(pitch_type, (0.8, 0.8, 0.8, 1.0))
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = base_color
        nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.8
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.2
    
    return mat

def register():
    pass

def unregister():
    pass