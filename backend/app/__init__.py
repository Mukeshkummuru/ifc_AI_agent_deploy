from flask import Flask
import os
from app.routes import main

def create_app():
    # Define absolute paths to frontend folders
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    template_dir = os.path.join(base_dir, 'backend', 'templates')
    static_dir = os.path.join(base_dir, 'backend', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    app.register_blueprint(main)
    
    return app
