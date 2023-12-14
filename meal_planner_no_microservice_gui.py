import json
import requests
import random
# from art import *
from tkinter import *
from tkinter import scrolledtext
from colorama import init, Fore, Style
import webbrowser
from docx import Document

init()

"""
----------------------------------------------------------------------------
Functions
----------------------------------------------------------------------------
"""


def color_text_green(text):
    return Fore.GREEN + text + Style.RESET_ALL


def color_text_red(text):
    return Fore.RED + text + Style.RESET_ALL


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


def create_recipe_document(recipe_list):
    # create new document
    doc = Document()
    # add heading
    doc.add_heading("Saved Recipes")

    # add each recipe to document
    for recipe_info in recipe_list[0]:
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


def create_ingredients_document(formatted_data):
    # create new document
    doc = Document()
    # add heading
    doc.add_heading("Ingredients List")

    # add each recipe to document
    for recipe_info in formatted_data[0]:
        for result_number, recipe_details in recipe_info.items():
            for recipe_ingredient in recipe_details['recipe']['ingredientLines']:
                doc.add_paragraph(f"{recipe_ingredient}")

    response_filename = 'Ingredients List.docx'
    doc.save(response_filename)


def browse_recipes():
    url = "https://www.allrecipes.com/"
    webbrowser.open(url)


def search_recipes():
    # global to store recipes
    new_data = {"hits": []}
    # create variables to store ingredients and saved recipes between loop runs
    ingredients = None
    selected_data = None
    food_list = None
    excluded_ingredients_str = excluded_ingredients_entry.get()
    ingredients = ingredients_entry.get()
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
            print(color_text_red(f"Your search for {ingredients} found no recipes, please try again."))
            food_list = None
    else:
        print("Please select at least one ingredient.\n")

    formatted_string = process_food_list(food_list)

    response = requests.get("https://api.edamam.com/api/recipes/v2?type=public&q=" + formatted_string +
                            "&app_id=2286dd85&app_key=1cdfcd395ccf99e349b18f54eaa4416f&" + excluded_ingredients_str +
                            "&random=true&field=url&field=label&field=ingredientLines")
    if response.status_code == 200:
        # parse the json
        dict_from_json = json.loads(response.text)
        if not dict_from_json["hits"]:
            print(color_text_red(f"Your search for {ingredients} found no recipes, please try again."))
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




"""
----------------------------------------------------------------------------
Main Program
----------------------------------------------------------------------------
"""

root = Tk()
root.title("Meal Planner")

# GUI Components
label = Label(root, text="Meal Planner")
label.pack()

instructions_label = Label(root, text="Enter ingredients to include (comma-separated):")
instructions_label.pack()

ingredients_entry = Entry(root, width=50)
ingredients_entry.pack()

excluded_ingredients_label = Label(root, text="Enter ingredients to exclude (comma-separated):")
excluded_ingredients_label.pack()

excluded_ingredients_entry = Entry(root, width=50)
excluded_ingredients_entry.pack()

num_recipes_label = Label(root, text="Enter the number of recipes (1 to 20):")
num_recipes_label.pack()

num_recipes_entry = Entry(root)
num_recipes_entry.pack()

button_frame = Frame(root)
button_frame.pack()

search_button = Button(button_frame, text="Search Recipes", command=search_recipes)
search_button.pack(side=LEFT)

browse_button = Button(button_frame, text="Browse Recipes", command=browse_recipes)
browse_button.pack(side=RIGHT)

output_text = scrolledtext.ScrolledText(root, width=70, height=50)
output_text.pack()

root.mainloop()
