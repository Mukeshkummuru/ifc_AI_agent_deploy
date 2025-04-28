import ifcopenshell
import os
import numpy as np
import ifcopenshell.geom

def load_ifc(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"IFC file not found at path: {filepath}")
    try:
        model = ifcopenshell.open(filepath)
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading IFC file: {e}")

def get_wall_count(model):
    try:
        walls = model.by_type("IfcWall")
        return len(walls)
    except AttributeError:
        return 0   

def get_plastering_area(model):
    walls = model.by_type("IfcWall")
    total_area = 0
    for wall in walls:
        area = extract_wall_area(wall)
        total_area += area
    return total_area

def extract_wall_area(wall):
     
    settings = ifcopenshell.geom.settings()
    settings.set("USE_WORLD_COORDS", True)

    try:
        shape = ifcopenshell.geom.create_shape(settings, wall)
        verts = np.array(shape.geometry.verts).reshape(-1, 3)
        faces = np.array(shape.geometry.faces).reshape(-1, 3)
        return calculate_surface_area(verts, faces)
    except Exception:
        return 0  

def calculate_surface_area(verts, faces):
    
    total = 0.0
    for face in faces:
        v1, v2, v3 = verts[face[0]], verts[face[1]], verts[face[2]]
        total += np.linalg.norm(np.cross(v2 - v1, v3 - v1)) / 2.0
    return total

def get_slab_volume(model):
    slabs = model.by_type("IfcSlab")
    total_volume = 0.0
    for slab in slabs:
        total_volume += extract_element_volume(slab)
    return total_volume

def get_wall_volume(model):
    walls = model.by_type("IfcWall")
    total_volume = 0.0
    for wall in walls:
        total_volume += extract_element_volume(wall)
    return total_volume

def extract_element_volume(element):
   
    if element.IsDefinedBy:
        for rel in element.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                props = rel.RelatingPropertyDefinition

               
                if hasattr(props, "HasProperties"):
                    for prop in props.HasProperties:
                        if hasattr(prop, "Name") and prop.Name in [
                            "NetVolume", "GrossVolume", "TotalVolume", "Volume"
                        ]:
                            try:
                                return float(prop.NominalValue.wrappedValue)
                            except Exception:
                                continue
    return 0.0


def get_door_count(model):
    try:
        doors = model.by_type('IfcDoor')
        return len(doors)
    except Exception as e:
        print(f"Error in get_door_count: {e}")
        return None

def get_material_names(model):
    materials = model.by_type("IfcMaterial")
    return [mat.Name for mat in materials if hasattr(mat, "Name")]