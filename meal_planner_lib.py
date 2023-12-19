import webbrowser
import requests
import random
import docx

#TODO: move function calls here
#TODO: figure out venv implementation so that installing packages aren't required


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
