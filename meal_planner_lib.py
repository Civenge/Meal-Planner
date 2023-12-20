import webbrowser
import requests
import random
import docx
import json
import requests
import random
from tkinter import *
from tkinter import scrolledtext, Tk, Button, messagebox
from docx import Document

#TODO: figure out venv implementation so that installing packages aren't required

"""
----------------------------------------------------------------------------
Globals
----------------------------------------------------------------------------
"""

# global to store recipes
new_data = {"hits": []}
selected_data = {"hits": []}





def create_recipe_document():
    total_recipes = []
    just_ingredients = []
    modified_data = [total_recipes, just_ingredients]

    # create new document
    doc = Document()
    # add heading
    doc.add_heading("Saved Recipes")

    for i, recipe_data in enumerate(new_data['hits'], start=1):
        # rename the recipe so they go in ascending order
        new_name = 'recipe ' + str(i)

        # create the new recipe dictionary
        new_recipe = {new_name: recipe_data}

        # add new recipe to list
        total_recipes.append(new_recipe)

        # isolate the ingredients list from the recipe
        new_ingredients = {new_name + ' ingredients': recipe_data['recipe']['ingredientLines']}

        # add isolated ingredients to list of ingredients
        just_ingredients.append(new_ingredients)

    # add each recipe to document
    for recipe_info in modified_data[0]:
        for result_number, recipe_details in recipe_info.items():
            title_paragraph = doc.add_paragraph()
            runner = title_paragraph.add_run(f"Recipe Title: {recipe_details['recipe']['label']}")
            runner.bold = True
            doc.add_paragraph(f"URL: {recipe_details['recipe']['url']}")

            # add ingredients as bulleted list
            doc.add_paragraph(f"Ingredients: ")
            for each_ingredient in recipe_details['recipe']['ingredientLines']:
                ingredient_paragraph = doc.add_paragraph(f"{each_ingredient}")
                ingredient_paragraph.style = 'List Bullet'

            doc.add_paragraph("\n")

    response_filename = 'Recipes.docx'
    doc.save(response_filename)




def create_ingredients_document():
    total_recipes = []
    just_ingredients = []
    modified_data = [total_recipes, just_ingredients]
    for i, recipe_data in enumerate(new_data['hits'], start=1):
        # rename the recipe so they go in ascending order
        new_name = 'recipe ' + str(i)

        # create the new recipe dictionary
        new_recipe = {new_name: recipe_data}

        # add new recipe to list
        total_recipes.append(new_recipe)

        # isolate the ingredients list from the recipe
        new_ingredients = {new_name + ' ingredients': recipe_data['recipe']['ingredientLines']}

        # add isolated ingredients to list of ingredients
        just_ingredients.append(new_ingredients)

    # create new document
    doc = Document()
    # add heading
    doc.add_heading("Ingredients List")

    # add each recipe to document
    for recipe_info in modified_data[0]:
        for result_number, recipe_details in recipe_info.items():
            for recipe_ingredient in recipe_details['recipe']['ingredientLines']:
                doc.add_paragraph(f"{recipe_ingredient}")

    response_filename = 'Ingredients List.docx'
    doc.save(response_filename)




def open_url(url):
    import webbrowser
    webbrowser.open(url)

def argument_handler(*args):
    if not args:
        return "You need to provide at least 1 argument."
    else:
        return list(args)


def remove_str_chars(input_string, num):
    if num >= 0:
        return input_string[:-num]
    else:
        return input_string


def process_food_list(input_list):
    request_string = ""
    for food in input_list:
        request_string = request_string + food + "%2c%20"
    # remove the last %2c%20 from the collated string which is unicode for ", "
    api_string = remove_str_chars(request_string, 6)
    return api_string


def browse_recipes():
    url = "https://www.allrecipes.com/"
    webbrowser.open(url)


def search_recipes(output_text, excluded_ingredients_entry, ingredients_entry, num_recipes_entry):
    global selected_data
    # clear existing text
    output_text.delete(1.0, END)
    excluded_ingredients_str = excluded_ingredients_entry.get()
    ingredients = ingredients_entry.get()
    if not ingredients:
        output_text.insert(END, "Please enter the number of recipes.\n")
        return
    num_recipes = int(num_recipes_entry.get())
    # Add your logic for searching recipes here
    if ingredients:
        food_list = argument_handler(ingredients)
        formatted_string = process_food_list(food_list)
        test_response = requests.get(
            "https://api.edamam.com/api/recipes/v2?type=public&q=" + formatted_string +
            "&app_id=2286dd85&app_key=1cdfcd395ccf99e349b18f54eaa4416f&random=true&field=url&field=label"
            "&field=ingredientLines")
        dict_from_json = json.loads(test_response.text)
        if not dict_from_json["hits"]:
            output_text.insert(END, f"Your search for {ingredients} found no recipes, please try again.")
            return
    else:
        output_text.insert(END, "Please select at least one ingredient.\n")
        return
    formatted_string = process_food_list(food_list)

    response = requests.get("https://api.edamam.com/api/recipes/v2?type=public&q=" + formatted_string +
                            "&app_id=2286dd85&app_key=1cdfcd395ccf99e349b18f54eaa4416f&" + excluded_ingredients_str +
                            "&random=true&field=url&field=label&field=ingredientLines")
    if response.status_code == 200:
        # parse the json
        dict_from_json = json.loads(response.text)
        if not dict_from_json["hits"]:
            output_text.insert(END, f"Your search for {ingredients} found no recipes, please try again.")
            exit(1)
        selected_recipes = random.sample(dict_from_json["hits"], num_recipes)
        selected_data = {
             "hits": selected_recipes
        }
        for i, recipe_data in enumerate(selected_data["hits"], start=1):
            recipe = recipe_data["recipe"]
            recipe_url = recipe["url"]
            recipe_name = recipe["label"]
            ingredients = recipe_data["recipe"]["ingredientLines"]

            # Append the recipe information to the text widget
            output_text.insert(END, f"Recipe{i}: {recipe_name}\n")
            output_text.insert(END, f"Url: {recipe_url}\n")

            for ingredient in ingredients:
                output_text.insert(END, f"  {ingredient}\n")

            output_text.insert(END, "\n")

    else:
        output_text.insert(END, f"API request failed with status code: {response.status_code}")