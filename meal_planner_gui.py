import json
from tkinter import *
from tkinter import scrolledtext, Tk, Button, messagebox
import requests
import meal_planner_lib
import random

"""
This project uses the edamam API to obtain recipes, with the API information below:
    api here: https://developer.edamam.com//admin/applications/1409623863337
    api doc: https://developer.edamam.com/edamam-docs-recipe-api

Requires installation of docx via "pip install python-docx" in console.
"""
global excluded_ingredients_entry
global ingredients_entry
global num_recipes_entry
global saved_recipes_entry
global root


"""
----------------------------------------------------------------------------
Functions
----------------------------------------------------------------------------
"""


def search_recipes(output_text, excluded_ingredients_entry_param, ingredients_entry_param, num_recipes_entry_param):
    # clear existing text
    output_text.delete(1.0, END)
    excluded_ingredients_str = excluded_ingredients_entry_param.get()
    ingredients = ingredients_entry_param.get()
    if not ingredients:
        show_error_message("Please enter the number of recipes.\n")
        return
    try:
        num_recipes = int(num_recipes_entry_param.get())
    except ValueError:
        show_error_message("Please input a valid number.\n")
        return
    if num_recipes <= 0 or num_recipes > 20:
        show_error_message("Please enter a valid positive number for the number of recipes (between 1 and 20).\n")
        return

    if ingredients:
        food_list = meal_planner_lib.argument_handler(ingredients)
        formatted_string = meal_planner_lib.process_food_list(food_list)
        response = requests.get("https://api.edamam.com/api/recipes/v2?type=public&q=" + formatted_string +
                                "&app_id=2286dd85&app_key=1cdfcd395ccf99e349b18f54eaa4416f&" + excluded_ingredients_str
                                + "&random=true&field=url&field=label&field=ingredientLines")
        dict_from_json = json.loads(response.text)
        if not dict_from_json["hits"]:
            output_text.insert(END, f"Your search for {ingredients} found no recipes, please try again.")
            return
    else:
        show_error_message("Please select at least one ingredient.\n")
        return

    if response.status_code == 200:
        # parse the json
        dict_from_json = json.loads(response.text)
        if not dict_from_json["hits"]:
            output_text.insert(END, f"Your search for {ingredients} found no recipes, please try again.")
            return
        selected_recipes = random.sample(dict_from_json["hits"], num_recipes)
        meal_planner_lib.selected_data = {
            "hits": selected_recipes
        }
        for i, recipe_data in enumerate(meal_planner_lib.selected_data["hits"], start=1):
            recipe = recipe_data["recipe"]
            recipe_url = recipe["url"]
            recipe_name = recipe["label"]
            ingredients = recipe_data["recipe"]["ingredientLines"]

            # append the recipe information to the text widget
            output_text.insert(END, f"Recipe{i}: {recipe_name}\n")
            output_text.insert(END, f"Url: {recipe_url}\n")

            for ingredient in ingredients:
                output_text.insert(END, f"  {ingredient}\n")

            output_text.insert(END, "\n")

    else:
        output_text.insert(END, f"API request failed with status code: {response.status_code}")


def save_recipes(output_text):
    saved_recipes = saved_recipes_entry.get()
    if not saved_recipes:
        show_error_message(f"Please select more than 0 recipes and make sure every selection is valid.\n")
        return
    split_values = saved_recipes.split(',')
    # remove whitespace in list
    current_saved_recipe_list = []
    for x in split_values:
        stripped_x = x.strip()
        current_saved_recipe_list.append(stripped_x)

    # removes non number values, but leaves a single negative sign if found (-)
    integer_list = []
    for x in current_saved_recipe_list:
        stripped_x = x.lstrip('-')
        if stripped_x.isdigit():
            integer_list.append(int(x))

    if int(min(integer_list)) <= 0:
        show_error_message(f"Please select more than 0 recipes and make sure every selection is valid.\n")
        return

    for val in current_saved_recipe_list:
        try:
            int(val)
        except ValueError:
            show_error_message("Please input a valid number.\n")
            return
        if int(val) < 0 or int(val) > len(meal_planner_lib.selected_data["hits"]):
            show_error_message(f"Please make sure your number is greater than 0 and less than total recipes "
                               f"searched.\n")
            return

    output_text.insert("1.0", f"Here is what you selected: {integer_list}\n")
    output_text.insert("2.0", "******* Adding recipes to saved recipes... *******\n\n")

    for idx in range(len(integer_list)):
        meal_planner_lib.new_data["hits"].append(meal_planner_lib.selected_data["hits"][integer_list[idx] - 1])

    return


def exit_app():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def show_help():
    help_window = Toplevel(root)
    help_window.title("Help")

    help_text = Text(help_window, width=70, height=20, wrap="word")
    help_text.pack()
    help_text.insert(INSERT, "The following link is a video to show how to use the Meal Planning App:\n\n")
    # add a tag for the URL link
    help_text.tag_configure("link", foreground="blue", underline=True)

    # insert the URL link with the "link" tag
    help_text.insert(INSERT, "Video demonstration\n\n", "link")

    # bind the click event to open the URL
    help_text.tag_bind("link", "<Button-1>", lambda event: meal_planner_lib.open_url("https://youtu.be/aXo--GO7ogc"))

    # insert the URL link with the "link" tag
    help_text.insert(INSERT, "This application is designed to be run from top to bottom.  Fill in each box and use the "
                             "associated buttons.  Using the buttons without having filled in the appropriate box with "
                             "valid information will lead to incorrect behavior.\n\n"
                             "Start by filling in the ingredients that you wish to have in your recipe.  Each "
                             "ingredient should be a single word.  For ingredients with multiple words, such as 'New "
                             "York Roast', enter them as 3 words 'New', 'York', and 'Roast'.\n\n"
                             "The 'Search Recipes' button will find recipes that match the criteria above.  If your "
                             "preference is instead to browse for a recipe, then this button will direct you to a "
                             "better resource to complete a browsing experience, as it falls outside the scope of this "
                             "project.\n\n")


def show_error_message(message):
    error_window = Toplevel(root)
    error_window.title("Error")

    bg_color = root.cget("bg")

    error_text = Text(error_window, width=50, height=5, font=('Times New Roman', 18, 'bold'), bg=bg_color, wrap="word")
    error_text.pack()

    error_text.insert(END, message)

    ok_button = Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack()

def show_new_data_contents():
    new_data_window = Toplevel(root)
    new_data_window.title("Saved Recipe Preview")

    new_data_text = Text(new_data_window, width=70, height=50, wrap="word")
    new_data_text.pack()

    for i, recipe_data in enumerate(meal_planner_lib.new_data["hits"], start=1):
        recipe = recipe_data["recipe"]
        recipe_url = recipe["url"]
        recipe_name = recipe["label"]
        ingredients = recipe_data["recipe"]["ingredientLines"]

        # append the recipe information to the text widget
        new_data_text.insert(END, f"Recipe{i}: {recipe_name}\n")
        new_data_text.insert(END, f"Url: {recipe_url}\n")

        for ingredient in ingredients:
            new_data_text.insert(END, f"  {ingredient}\n")

        new_data_text.insert(END, "\n")

        font_tuple = ("Times New Roman", 12)
        new_data_text.configure(font=font_tuple)


"""
----------------------------------------------------------------------------
Main Program
----------------------------------------------------------------------------
"""


def main():
    global excluded_ingredients_entry
    global ingredients_entry
    global num_recipes_entry
    global saved_recipes_entry
    global root

    def _create_recipe_document():
        meal_planner_lib.create_recipe_document()
        output_text.insert(END, "Creating 'Recipes.docx' file...\n")

    def _create_ingredients_document():
        meal_planner_lib.create_ingredients_document()
        output_text.insert(END, "Creating 'Ingredients List.docx' file...\n")

    root = Tk()
    root.title("Meal Planner")

    bg_color = root.cget("bg")

    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=show_help)

    header_text = Text(root, height=1, width=len("Meal Planner App"), font=('Times New Roman', 48, 'bold'), bg=bg_color)
    header_text.insert(INSERT, "Meal Planner App!")
    header_text.tag_configure("center", justify=CENTER)
    header_text.tag_add("center", 1.0, "end")
    header_text.pack()

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

    search_button = Button(button_frame, text="Search Recipes",
                           command=lambda: search_recipes(output_text, excluded_ingredients_entry,
                                                          ingredients_entry, num_recipes_entry))
    search_button.pack(side=LEFT)

    browse_button = Button(button_frame, text="Browse Recipes", command=meal_planner_lib.browse_recipes)
    browse_button.pack(side=RIGHT)

    saved_recipes_label = Label(root, text="Enter recipe numbers to save (Ex: 1, 2, 4)")
    saved_recipes_label.pack()

    saved_recipes_entry = Entry(root)
    saved_recipes_entry.pack()

    button_frame_save_recipes = Frame(root)
    button_frame_save_recipes.pack()

    save_recipe_button = Button(button_frame_save_recipes, text="Save Recipes",
                                command=lambda: save_recipes(output_text))
    save_recipe_button.pack(side=LEFT)

    show_saved_recipes_preview_button = Button(button_frame_save_recipes, text="Preview of Saved Recipes", command=show_new_data_contents)
    show_saved_recipes_preview_button.pack()

    button_frame_export_word = Frame(root)
    button_frame_export_word.pack()

    export_recipe_to_word_button = Button(button_frame_export_word, text="Export Saved Recipes to Word",
                                          command=_create_recipe_document)
    export_recipe_to_word_button.pack(side=LEFT)

    export_ingredients_to_word_button = Button(button_frame_export_word, text="Export Saved Ingredients to Word",
                                               command=_create_ingredients_document)
    export_ingredients_to_word_button.pack(side=RIGHT)

    exit_button = Button(root, text="Exit", command=exit_app)
    exit_button.pack()

    output_text = scrolledtext.ScrolledText(root, width=70, height=40)
    output_text.pack()

    font_tuple = ("Times New Roman", 12)
    output_text.configure(font=font_tuple)

    root.mainloop()


if __name__ == "__main__":
    main()
