# Meal-Planner
This application helps a user discover new recipes based upon user input.  Users are allowed to choose ingredients to include, ingredients to exclude, how many recipes they want to view, and then select from a list of recipes which they would like to save.  It will continue to allow for searches of different parameters until the user decides they have enough results.  Saving of recipes will persist between each search.  Once a user is complete with searching and selecting recipes they want to save, the user can then export all saved recipes into a Microsoft Word .docx format as recipes, ingredients lists, or both.

# Running GUI in Virtual Environment
In the folder where you cloned the repo, open the Python terminal and run:  
"venv\Scripts\activate"  
Then install the correct dependancies by running:  
"pip install -r requirements.txt"  
Finally run the application as you normally would, or from the terminal type:  
"python .\meal_planner_gui.py"

# Demo Video of Meal Planner App GUI Version
[![Meal Planner GUI](https://img.youtube.com/vi/-4FxLinui0Q/0.jpg)](https://www.youtube.com/watch?v=-4FxLinui0Q)

# Recipe Data
All recipe data is gathered based upon a custom API request to Edamam.  Each search yields a random result, so a user is unlikely to see the same recipe twice even given the same input.  The api can be found at: https://developer.edamam.com//admin/applications/1409623863337 with documentation located at: https://developer.edamam.com/edamam-docs-recipe-api

# CLI version
This is a Command Line Interface version of the App.  This will allow for a fast, efficient way to search for and store new recipes.

# GUI Version
This is a Graphical User Interface Version which supports the functionality of the CLI version with additional features added in simple to understand format.  This is the version shown in the video linked above.
