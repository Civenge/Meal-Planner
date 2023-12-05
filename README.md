# Meal-Planner
This application helps a user discover new recipes based upon user input.  Users are allowed to choose ingredients to include, ingredients to exclude, how many recipes they want to view, and then select from a list of recipes which they would like to save.  It will continue to allow for searches of different parameters until the user decides there are enough results.  Once a user is complete with the searching and selecting recipes they want to save, the user can then export the results into a Microsoft Word .docx format as recipes, ingredients lists, or both.  

# Recipe Data
All recipe data is gathered based upon a custom API request to Edamam.  Each search yields a random result, so a user is unlikely to see the same recipe twice even given the same input.  The api can be found at: https://developer.edamam.com//admin/applications/1409623863337 with documentation located at: https://developer.edamam.com/edamam-docs-recipe-api

# Microservice
This application utilizes a microservice to process the recipe JSON data which returns a list of the recipe data and ingredients.  

# Non-Microservice Version
This is the same code but without the microservice functionality, which drastically speeds up the application.  Download the meal_planner_no_microservice.zip, extract and run the meal_planner_no_microservice.exe file.

Alternatively, to convert meal_planner_no_microservice.py to a Windows executable, install pyinstaller "pip install pyinstaller" in the console and then run the following command in the directory of the python file:

pyinstaller --onefile meal_planner_no_microservice.py

**UML Diagram Showing the Microservice Data Flow**

![image](https://github.com/Civenge/Meal-Planner/assets/91363144/a76238e3-f01a-4aec-9a42-342907a62aa1)
