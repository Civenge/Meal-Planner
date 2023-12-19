# Meal-Planner
This application helps a user discover new recipes based upon user input.  Users are allowed to choose ingredients to include, ingredients to exclude, how many recipes they want to view, and then select from a list of recipes which they would like to save.  It will continue to allow for searches of different parameters until the user decides they have enough results.  Saving of recipes will persist between each search.  Once a user is complete with searching and selecting recipes they want to save, the user can then export all saved recipes into a Microsoft Word .docx format as recipes, ingredients lists, or both.

# Video of Meal Planner App
https://www.youtube.com/watch?v=aXo--GO7ogc

# Recipe Data
All recipe data is gathered based upon a custom API request to Edamam.  Each search yields a random result, so a user is unlikely to see the same recipe twice even given the same input.  The api can be found at: https://developer.edamam.com//admin/applications/1409623863337 with documentation located at: https://developer.edamam.com/edamam-docs-recipe-api

# CLI version.
This is a Command Line Interface version of the App.  This will allow for a fast, efficient way to search for and store new recipes.

To convert meal_planner_cli.py to a Windows executable file, install pyinstaller "pip install pyinstaller" in the console and then run the following command in the directory of the python file:

pyinstaller --onefile meal_planner_cli.py

# GUI Version
This is a Graphical User Interface Version which supports the same functionality of the CLI version in simple to understand format.  This is the version shown in the video linked above.

To convert meal_planner_gui.py to a Windows executable file, install pyinstaller "pip install pyinstaller" in the console and then run the following command in the directory of the python file:

pyinstaller --onefile meal_planner_gui.py
