from flask import Blueprint

# Blueprint imports
from .home import home_bp
from .ingredient_fetcher import ingredient_fetcher_bp
from .recipe_curation import recipe_curation_bp
from .waste_repurpose import waste_repurpose_bp
from .manual_recipe_input import manual_recipe_input_bp
from .manual_waste_input import manual_waste_input_bp


def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(ingredient_fetcher_bp)
    app.register_blueprint(recipe_curation_bp)
    app.register_blueprint(manual_recipe_input_bp)
    app.register_blueprint(manual_waste_input_bp)
    app.register_blueprint(waste_repurpose_bp)
