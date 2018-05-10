""" Open Food Facts API function """
import urllib.request
import json
from food.models import Categorie

def get_product(search):
    """ Get some substitute """
    # Download the the product list from the search word
    search = search.capitalize()
    result_url = urllib.request.urlopen(
        'https://fr.openfoodfacts.org/cgi/search.pl?search_terms='+ search +'&json=1&page_size=20&search_simple=1')
    data = result_url.read()
    json_output = json.loads(data.decode("UTF-8"))
    if json_output["count"] >= 1:
        # Extract the categorie list and nutrition grade from the product list
        categorie = []
        try:
            categorie = json_output["products"][0]["categories"].split(',')
        except:
            categorie_list = json_output["products"][0]["categories_tags"]
            categorie = [item[3:] for item in categorie_list if item[:2] == "fr"]
        
        nutrition_grade = json_output["products"][0]["nutrition_grades"]
        result = categorie, nutrition_grade
        return result
    else:
        # No result
        return None

def get_result(categorie, nutrition_grade, page=1):
    cat = categorie[0]
    # On va récupérer la liste des produits correspondant
    categorie_match = Categorie.objects.get(categorie_name=cat)
    data_url = urllib.request.urlopen(categorie_match.categorie_url + '/' + str(page) + '.json')
    data = data_url.read()
    json_data = json.loads(data.decode("UTF-8"))
    json_lenght = json_data["page_size"]
    product = {}
    item_count = 0
    for rank in range(0, json_lenght):
        if "nutrition_grades" in json_data["products"][rank]:
            if json_data["products"][rank]["nutrition_grades"] <= nutrition_grade:
                if "image_front_url" in json_data["products"][rank]:
                    product[item_count] = []
                    product[item_count].append(json_data["products"][rank]["image_front_url"])
                    product[item_count].append(json_data["products"][rank]["nutrition_grades"])
                    product[item_count].append(json_data["products"][rank]["product_name"])
                    item_count += 1
                else:
                    continue
            else:
                continue
        else:
            continue
            
    return json.dumps(product)
