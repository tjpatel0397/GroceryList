from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load recipes from JSON file
def load_recipes():
    with open('recipes.json', 'r') as file:
        return json.load(file)

# Home route to display recipes
@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = load_recipes()
    if request.method == 'POST':
        selected_recipes = request.form.getlist('recipes')
        selected_recipes = [int(i) for i in selected_recipes]
        return redirect(url_for('grocery_list', selections=selected_recipes))
    return render_template('index.html', recipes=recipes)

# Route to display the grocery list
@app.route('/grocery_list')
def grocery_list():
    try:
        selections = request.args.getlist('selections', type=int)
        recipes = load_recipes()

        # Debugging output
        print(f"Selections: {selections}")
        print(f"Recipes: {recipes}")

        if not isinstance(recipes, dict):
            return "Recipes data is not a dictionary", 500

        grocery_items = {}

        for idx in selections:
            str_idx = str(idx)  # Convert index to string to match dictionary keys
            if str_idx not in recipes:
                return "Invalid recipe selection", 400  # Bad Request if index is not a valid key
            recipe = recipes[str_idx]
            for ingredient in recipe['ingredients']:
                item = ingredient['item']
                quantity = ingredient.get('quantity', '')
                if item in grocery_items:
                    grocery_items[item].append(quantity)
                else:
                    grocery_items[item] = [quantity]

        # Consolidate quantities
        consolidated_list = []
        for item, quantities in grocery_items.items():
            quantities = [q for q in quantities if q]
            quantity_str = ', '.join(quantities) if quantities else ''
            consolidated_list.append({'item': item, 'quantity': quantity_str})

        return render_template('grocery_list.html', grocery_list=consolidated_list)
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
