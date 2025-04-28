from flask import Blueprint, render_template, request, jsonify
from app.nlp import preprocess_input, identify_intent
from app.ifc_utils import (
    load_ifc,
    get_wall_count,
    get_plastering_area,
    get_slab_volume,
    get_wall_volume,
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

        model = load_ifc('backend/assignment.ifc')
        if not model:
            return jsonify({'response': 'Failed to load IFC file.'})

        if intent == 'plastering_area':
            area = get_plastering_area(model)
            response = f"Total plastering area is {area:.2f} square meters."

        elif intent == 'wall_area':
            area =  get_plastering_area(model)  # Assuming same logic
            response = f"The total wall surface area is approximately {area:.2f} square meters."

        elif intent == 'wall_count':
            count = get_wall_count(model)
            response = f"There are {count} walls in the model."

        elif intent == 'wall_volume':
            volume = get_wall_volume(model)
            response = f"Total volume of all walls is {volume:.2f} cubic meters."

        elif intent == 'slab_volume':
            slab_volume = get_slab_volume(model)
            response = f"The total slab volume is approximately {slab_volume:.2f} cubic meters."

        else:
            response = "I'm sorry, I didn't understand that."

        return jsonify({'response': response})
    
    except Exception as e:
        # Print error to server log
        print(f"🔥 Error in /query: {e}")
        return jsonify({'response': f"bot: error occurred ({str(e)})"})
