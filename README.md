# Blender PitchViz

A Blender add-on for visualizing baseball pitch trajectories using MLB Statcast data. This plugin allows you to create 3D visualizations of pitch movement similar to Baseball Savant's 3D pitch visualization tool.

## Features

- Import Statcast pitch data from CSV files
- Visualize pitch trajectories in 3D space
- Generate a regulation-sized strike zone
- Group pitches by at-bat for easy analysis
- Color-code pitches by type (fastball, slider, etc.)
- Accurate physics-based trajectory calculations using Statcast data

## Installation

1. Download the latest release ZIP file
2. Open Blender and go to Edit > Preferences > Add-ons
3. Click "Install..." and select the downloaded ZIP file
4. Enable the add-on by checking the box next to "Visualization: Blender PitchViz"

## Usage

### Importing Pitch Data

1. Prepare your Statcast data as a CSV file with the following required columns:
   - `pitch_type`: Type of pitch (FF, CU, SL, etc.)
   - `release_pos_x`, `release_pos_y`, `release_pos_z`: Release point coordinates
   - `vx0`, `vy0`, `vz0`: Initial velocities
   - `ax`, `ay`, `az`: Acceleration components
   - `plate_x`, `plate_z`: Position at home plate
   - `at_bat_number`: For grouping pitches (optional)

2. In Blender's 3D Viewport, find the "Statcast" tab in the sidebar (press N if sidebar is hidden)
3. Click "Select Statcast CSV" and choose your data file

### Visualizing Pitches

1. After importing data, click "Visualize Pitches"
2. Optional features:
   - Check "Group by At-Bat" to organize pitches in collections
   - Check "Assign Pitch Materials" to color-code by pitch type
3. Click "Create Strike Zone" to add a reference strike zone

### Pitch Colors

- Four-seam Fastball (FF): Red
- Sinker (SI): Orange
- Curveball (CU): Blue
- Slider (SL): Yellow
- Changeup (CH): Green
- Cutter (FC): Purple

## Development

### Project Structure

```
blender-pitchviz/
├── __init__.py          # Add-on initialization and registration
├── operators.py         # Blender operators for user actions
├── panels.py           # UI panel definitions
└── visualize.py        # Core visualization logic
```

### Technical Details

- Uses Statcast physics data to calculate accurate pitch trajectories
- Converts coordinates from feet (Statcast) to meters (Blender)
- Creates smooth NURBS curves for pitch visualization
- Implements MLB regulation strike zone dimensions

## Requirements

- Blender 3.0.0 or newer
- Statcast data in CSV format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your chosen license]

## Acknowledgments

- MLB Statcast for providing pitch tracking data
- Baseball Savant for inspiration and reference visualizations

## Author

Liam O'Mahony

## Version History

- 0.1.0: Initial release
  - Basic pitch visualization
  - Strike zone creation
  - Pitch grouping and coloring features
