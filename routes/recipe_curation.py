from flask import Blueprint, render_template, request
import pandas as pd
from rapidfuzz import fuzz

recipe_curation_bp = Blueprint('recipe_curation', __name__)

# Load and preprocess recipe data
df = pd.read_csv('data/processed_recipes.csv')
df['ingredients'] = df['ingredients'].apply(
    lambda x: [i.strip().lower() for i in str(x).split(',')] if pd.notnull(x) else []
)

@recipe_curation_bp.route('/recipe-curation', methods=['POST'])
def recipe_curation():
    # Retrieve form data
    detected_ingredients = [i.lower().strip() for i in request.form.getlist('ingredients')]
    dietary_pref = request.form.get('dietary_preference', '').strip().lower()
    cuisine = request.form.get('cuisine', '').strip().lower()
    meal_type = request.form.get('meal_type', '').strip().lower()
    skill_level = request.form.get('skill_level', '').strip().lower()

    matched_recipes = []

    for _, row in df.iterrows():
        recipe_ingredients = row['ingredients']

        # Use fuzzy matching to compare user ingredients with recipe ingredients
        fuzzy_matches = []
        for user_ingredient in detected_ingredients:
            for recipe_ingredient in recipe_ingredients:
                if fuzz.partial_ratio(user_ingredient, recipe_ingredient) >= 70:
                    fuzzy_matches.append(recipe_ingredient)
                    break  # Avoid duplicate counting

        if len(fuzzy_matches) >= 2:  # Adjust threshold here
            match_score = 0
            if dietary_pref in str(row.get('dietary_preferences', '')).lower(): match_score += 1
            if cuisine in str(row.get('cuisine', '')).lower(): match_score += 1
            if meal_type in str(row.get('meal_type', '')).lower(): match_score += 1
            if skill_level in str(row.get('skill_level', '')).lower(): match_score += 1

            if match_score >= 1:
                matched_recipes.append({
                    'title': row.get('name', 'Unnamed Recipe'),
                    'ingredients': recipe_ingredients,
                    'dietary_preferences': row.get('dietary_preferences', ''),
                    'cuisine': row.get('cuisine', ''),
                    'meal_type': row.get('meal_type', ''),
                    'skill_level': row.get('skill_level', ''),
                    'instructions': row.get('description', 'No instructions provided.')
                })

        # Stop once 3 matching recipes are found
        if len(matched_recipes) == 3:
            break

    return render_template('recipe_curation.html',
                           ingredients=detected_ingredients,
                           dietary_preference=dietary_pref,
                           cuisine=cuisine,
                           meal_type=meal_type,
                           skill_level=skill_level,
                           matched_recipes=matched_recipes)
