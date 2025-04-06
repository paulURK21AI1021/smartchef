from flask import Flask, render_template
from flask import Flask, render_template, request
from routes.ingredient_fetcher import ingredient_fetcher_bp
from routes.recipe_curation import recipe_curation_bp
from routes.waste_repurpose import waste_repurpose_bp
from routes.manual_recipe_input import manual_recipe_input_bp
from routes.manual_waste_input import manual_waste_input_bp




app = Flask(__name__)

# Registering blueprints
app.register_blueprint(ingredient_fetcher_bp)
app.register_blueprint(recipe_curation_bp)
app.register_blueprint(waste_repurpose_bp)
app.register_blueprint(manual_recipe_input_bp)
app.register_blueprint(manual_waste_input_bp)


@app.before_request
def show_routes():
    print("\n🚀 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint} => {rule.rule}")

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
