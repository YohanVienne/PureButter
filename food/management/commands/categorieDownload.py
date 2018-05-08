import urllib.request
import json
from food.models import Categorie
from django.core.management.base import BaseCommand

 

class Command(BaseCommand):
    help = "Download the French categorie and insert/update it to the database"

    def handle(self, *args, **options):
        try:
            # Get the french categorie database from OpenFoodFacts and add to the local database
            print("Downloading...")
            categories_url = urllib.request.urlopen(
                'https://fr.openfoodfacts.org/categories.json')
            data = categories_url.read()
            json_output = json.loads(data.decode("UTF-8"))
            self.stdout.write("Insertion in database...")
            # Change the type to str format, control len size and take of the langage prefixe(Cleaning file)
            for categorie in json_output["tags"]:
                cat_name = categorie['name']
                cat_name = cat_name.replace("'", " ")
                if (len(cat_name) >= 76) or (len(categorie['url']) >= 151):
                    continue
                if cat_name[2:3] == ":":
                    continue
                if len(cat_name) == 0:
                    continue
                if Categorie.objects.filter(categorie_name=cat_name):
                    continue

                cat = Categorie(categorie_name=cat_name,
                                categorie_url=categorie['url'])
                cat.save()
            self.stdout.write("Download done with {} categories".format(
                Categorie.objects.count()))
        except Exception as e:
            self.stdout.write("An error is occured: {}".format(e))
