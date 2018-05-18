""" Open Food Facts API function """
import requests
import json
from food.models import Categorie


def get_product(search):
    """ Get some substitute """
    # Download the the product list from the search word
    search = search.capitalize()
    try:
        payload = {'json': '1', 'page_size': '20', 'search_simple': '1'}
        result_url = requests.get(
            'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=' + search, params=payload)
        data = result_url.json()
        # Extract the categorie list and nutrition grade from the product list
        categorie = []
        for product_count in range(int(data["page_size"])):
            try:
                categorie = data["products"][product_count]["categories"].split(',')
                if categorie[0][2:3] == ":":
                    categorie = [item[3:] for item in categorie if item[:2] == "fr"]
            except:
                categorie_list = data["products"][product_count]["categories_tags"]
                categorie = [item[3:] for item in categorie_list if item[:2] == "fr"]
            if len(categorie) >= 1:
                print("categorie: " + str(categorie))
                nutrition_grade = data["products"][product_count]["nutrition_grades_tags"]
                result = categorie, nutrition_grade
                return result
    except:
        # No result
        return None


def get_result(categorie, nutrition_grade):
    cat = categorie[(len(categorie)-1)]
    try:
        categorie_match = Categorie.objects.get(categorie_name=cat)
    except:
        cat_url = cat.replace(' ', '-')
        categorie_match = Categorie.objects.get(categorie_name=cat_url)[:1]
    print('cat_match: ' + str(categorie_match))
    data_url = requests.get(categorie_match.categorie_url + '.json')
    data = data_url.json()
    json_lenght = data["count"]
    if json_lenght > 20:
        json_lenght = 20
    product = []
    item_count = 0
    for rank in range(0, json_lenght):
        if "nutrition_grades_tags" in data["products"][rank]:
            if data["products"][rank]["nutrition_grades_tags"] <= nutrition_grade:
                if "image_front_url" in data["products"][rank]:
                    temp_list = []
                    temp_list.append(data["products"][rank]["image_front_url"])
                    temp_list.append(data["products"][rank]["nutrition_grades_tags"][0])
                    temp_list.append(data["products"][rank]["product_name"])
                    temp_list.append(data["products"][rank]["url"])
                    nutriment = data["products"][rank]["nutriments"]
                    tmpIngredient = []
                    tmpIngredient = {key[:len(key)-5]: value for (key, value)
                                  in nutriment.items() if key[len(key)-5:] == '_100g'}
                    ingredient = {key: value for (key, value)
                                  in tmpIngredient.items() if key[:len(key)-9] != 'nutrition'}
                    temp_list.append(ingredient)
                    temp_list.append(item_count)
                    product.append(temp_list)
                    item_count += 1
                    if item_count == 6:
                        break
                else:
                    continue
            else:
                continue
        else:
            continue
    return json.dumps(product)

"""
Dict
0 image
1 nutrition
2 name
3 url
4 ingredient
5 count
"""
