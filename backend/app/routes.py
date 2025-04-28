from flask import Blueprint, render_template, request, jsonify
from app.nlp import preprocess_input, identify_intent
from app.ifc_utils import (
    load_ifc,
    get_wall_count,
    get_plastering_area,
    get_slab_volume,
    get_wall_volume,
    get_door_count,
    get_material_names,
)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        tokens = preprocess_input(user_input)
        intent = identify_intent(tokens)

        if intent == 'greeting':
            return jsonify({'response': "Hello! How can I assist you with your building model?"})

        model = load_ifc('backend/assignment.ifc')
        if not model:
            return jsonify({'response': 'Failed to load IFC file.'})

        if intent == 'plastering_area':
            area = get_plastering_area(model)
            response = f"Total plastering area is {area:.2f} square meters." if area is not None else "Couldn't calculate plastering area."

        elif intent == 'wall_area':
            area =  get_plastering_area(model)  
            response = f"The total wall surface area is approximately {area:.2f} square meters." if area is not None else "Couldn't calculate wall surface area."

        elif intent == 'wall_count':
            count = get_wall_count(model)
            response = f"There are {count} walls in the model." if count is not None else "Couldn't retrieve wall count."

        elif intent == 'wall_volume':
            volume = get_wall_volume(model)
            response = f"Total volume of all walls is {volume:.2f} cubic meters." if volume is not None else "Couldn't calculate wall volume."

        elif intent == 'slab_volume':
            slab_volume = get_slab_volume(model)
            response = f"The total slab volume is approximately {slab_volume:.2f} cubic meters."  if slab_volume is not None else "Couldn't calculate slab volume."

        elif intent == 'door_count':
            door_count = get_door_count(model)
            if door_count is None:
                response = "Unable to count doors. Please check the model data."
            else:
                response = f"There are {door_count} doors in the model."
            
        elif intent == 'material_names':
            material_names = get_material_names(model)
            response = "The materials used in this project are: " + ", ".join(material_names)  if material_names is not None else "materials are not found in the data"

        else:
            response = "I'm sorry, I didn't understand that. Could you please rephrase?"

        return jsonify({'response': response})
    
    except Exception as e:
        print(f"🔥 Error in /query: {e}")
        return jsonify({'response': f"bot: error occurred ({str(e)})"})