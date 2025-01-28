bl_info = {
    "name": "Blender_pitchviz",
    "author": "Liam O'Mahony",
    "description": "Visualize baseball pitches in 3D using Statcast data.",
    "blender": (3, 0, 0),
    "version": (0, 1, 0),
    "location": "View3D > UI",
    "warning": "",
    "category": "Visualization",
}

import bpy
from . import operators
from . import panels
from . import visualize

def register():
    operators.register()
    panels.register()
    visualize.register()

def unregister():
    visualize.unregister()
    panels.unregister()
    operators.unregister()

if __name__ == "__main__":
    register()