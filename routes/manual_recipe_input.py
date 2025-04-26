from flask import Blueprint, render_template, request
import pandas as pd
from rapidfuzz import fuzz

manual_recipe_input_bp = Blueprint('manual_recipe_input', __name__)

# Load recipe data
df = pd.read_csv('data/processed_recipes.csv')
df['ingredients'] = df['ingredients'].apply(
    lambda x: [i.strip().lower() for i in str(x).split(',')] if pd.notnull(x) else []
)

@manual_recipe_input_bp.route('/manual-recipe-input', methods=['GET'])
def show_manual_recipe_form():
    return render_template('manual_recipe_input.html')

@manual_recipe_input_bp.route('/manual-recipe-input', methods=['POST'])
def manual_recipe_input():
    matched_recipes = []

    if request.method == 'POST':
        ingredients_raw = request.form.get('manual_ingredients', '')
        detected_ingredients = [i.strip().lower() for i in ingredients_raw.split(',') if i.strip()]

        dietary_pref = request.form.get('dietary_preference', '').strip().lower()
        cuisine = request.form.get('cuisine', '').strip().lower()
        meal_type = request.form.get('meal_type', '').strip().lower()
        skill_level = request.form.get('skill_level', '').strip().lower()

        for _, row in df.iterrows():
            recipe_ingredients = row['ingredients']
            fuzzy_matches = []

            for user_ing in detected_ingredients:
                for recipe_ing in recipe_ingredients:
                    if fuzz.partial_ratio(user_ing, recipe_ing) >= 70:
                        fuzzy_matches.append(recipe_ing)
                        break

            if len(fuzzy_matches) >= 2:
                match_score = 0
                if dietary_pref in str(row.get('dietary_preferences', '')).lower(): match_score += 1
                if cuisine in str(row.get('cuisine', '')).lower(): match_score += 1
                if meal_type in str(row.get('meal_type', '')).lower(): match_score += 1
                if skill_level in str(row.get('skill_level', '')).lower(): match_score += 1

                if match_score >= 1:
                    # Parse nutrition into a dictionary
                    nutrition_info = {}
                    if pd.notnull(row.get('nutrition', '')):
                        nutrition_parts = str(row.get('nutrition', '')).split(',')
                        for part in nutrition_parts:
                            if ':' in part:
                                key, value = part.split(':', 1)
                                nutrition_info[key.strip()] = value.strip()

                    matched_recipes.append({
                        'title': row.get('name', 'Unnamed Recipe'),
                        'ingredients': recipe_ingredients,
                        'dietary_preferences': row.get('dietary_preferences', ''),
                        'cuisine': row.get('cuisine', ''),
                        'meal_type': row.get('meal_type', ''),
                        'skill_level': row.get('skill_level', ''),
                        'instructions': row.get('steps', 'No instructions provided.'),
                        'nutrition': nutrition_info  # <<< Added nutrition here
                    })

            if len(matched_recipes) == 3:
                break

        return render_template('manual_recipe_input.html',
                               matched_recipes=matched_recipes)

    return render_template('manual_recipe_input.html', matched_recipes=None)
