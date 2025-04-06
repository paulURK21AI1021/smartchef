from flask import Blueprint, render_template, request
import pandas as pd
from rapidfuzz import fuzz

manual_waste_input_bp = Blueprint('manual_waste_input', __name__)

# Load CSV file with correct column names
df = pd.read_csv('data/WasteManagementData .csv')
df['Ingredient Name'] = df['Ingredient Name'].apply(lambda x: x.strip().lower())

@manual_waste_input_bp.route('/manual-waste-input', methods=['GET', 'POST'])
def manual_waste_input():
    if request.method == 'POST':
        # existing logic to handle form submission
        waste_items = [item.strip().lower() for item in request.form.get('waste_items', '').split(',')]
        suggestions = []

        for user_item in waste_items:
            for _, row in df.iterrows():
                db_item = row['Ingredient Name']
                if fuzz.partial_ratio(user_item, db_item) >= 70:
                    suggestions.append({
                        'ingredient': db_item.title(),
                        'edibility': row.get('Edible/ Non-Edible', 'Unknown'),
                        'tips': row.get('Suggestions', 'No suggestions provided.')
                    })
                    break

        return render_template('manual_waste_output.html', suggestions=suggestions)
    
    # 👉 GET request — show the form
    return render_template('manual_waste_input.html')
