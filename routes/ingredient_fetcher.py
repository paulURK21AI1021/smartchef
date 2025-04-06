from flask import Blueprint, render_template, request
import pandas as pd
import os
from werkzeug.utils import secure_filename

ingredient_fetcher_bp = Blueprint('ingredient_fetcher', __name__)
UPLOAD_FOLDER = 'static/uploads'

@ingredient_fetcher_bp.route('/ingredient-fetcher', methods=['GET', 'POST'])
def ingredient_fetcher():
    ingredients_data = []
    if request.method == 'POST':
        files = request.files.getlist('images')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        df = pd.read_csv('data/IngredientList.csv')

        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

                image_id = os.path.splitext(filename)[0]
                match = df[df['Image Name'].str.upper() == image_id.upper()]
                if not match.empty:
                    ingredients = match.iloc[0]['Ingredient List']
                    ingredients_list = [item.strip() for item in ingredients.split(',')]
                else:
                    ingredients_list = ["No ingredients found."]

                ingredients_data.append({
                    'image_url': file_path,
                    'ingredients': ingredients_list
                })

    return render_template('ingredient_fetcher.html', ingredients_data=ingredients_data)
