from flask import Blueprint, render_template, request
import pandas as pd
from rapidfuzz import fuzz

waste_repurpose_bp = Blueprint('waste_repurpose', __name__)

# Load waste management suggestions
waste_df = pd.read_csv('data/WasteManagementData .csv')
waste_df['Ingredient Name'] = waste_df['Ingredient Name'].str.lower().str.strip()

@waste_repurpose_bp.route('/waste-repurpose', methods=['POST'])
def waste_repurpose():
    user_ingredients = [i.lower().strip() for i in request.form.getlist('ingredients')]

    suggestions_output = []

    for user_ing in user_ingredients:
        best_match = None
        best_score = 0

        for _, row in waste_df.iterrows():
            waste_ing = row['Ingredient Name']
            score = fuzz.partial_ratio(user_ing, waste_ing)

            if score > best_score and score >= 70:  # threshold can be adjusted
                best_score = score
                best_match = row

        if best_match is not None:
            suggestions_output.append({
                'ingredient': best_match['Ingredient Name'].title(),
                'edibility': best_match['Edible/ Non-Edible'],
                'suggestions': best_match['Suggestions']
            })

    return render_template('waste_repurpose.html', suggestions=suggestions_output)
