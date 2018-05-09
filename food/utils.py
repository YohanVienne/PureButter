""" Open Food Facts API function """
import urllib.request
import json
from .models import Categorie, Product

def get_result(search):
    """ Get some substitute """
    # Download the the product list from the search word
    search = search.capitalize()
    result_url = urllib.request.urlopen(
        'https://fr.openfoodfacts.org/cgi/search.pl?search_terms='+ search +'&json=1&page_size=20&search_simple=1')
    data = result_url.read()
    json_output = json.loads(data.decode("UTF-8"))
    # Extract the categorie list and nutrition grade from the product list
    categorie = []
    try:
        categorie = json_output["products"][0]["categories"].split(',')
    except:
        categorie_list = json_output["products"][0]["categories_tags"]
        categorie = [item[3:] for item in categorie_list if item[:2] == "fr"]
    
    nutrition_grade = json_output["products"][0]["nutrition_grades"]
    return categorie, nutrition_grade