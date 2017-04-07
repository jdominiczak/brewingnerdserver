from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from brewery.models import Hop, Misc, Yeast, Fermentable, Water

class RecipeTests(APITestCase):
    def test_create_ingredients(self):
        """
        Ensure we can create and delete each ingredient
        """
        url = '/hops/'
        data = {'type':'Bittering', 'form': 'Pellet', 'name': 'Cascade', 'default_alpha':'5.5'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hop.objects.count(), 1)
        self.assertEqual(Hop.objects.get().name, 'Cascade')
        
        # miscs
        url = '/miscs/'
        data = {
        "type": "Fining",
        "name": "Irish Moss",
        "use_for": "Clarifying Agent",
        "notes": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Misc.objects.count(), 1)
        self.assertEqual(Misc.objects.get().name, 'Irish Moss')
        
        # yeasts
        url = '/yeasts/'
        data = {
            "type": "Wheat",
            "form": "Liquid",
            "flocculation": "Low",
            "name": "Belgian Wit Ale",
            "laboratory": "White Labs",
            "product_id": "WLP400",
            "min_temperature": "19.4444",
            "max_temperature": "23.3333",
            "attenuation": "76.0",
            "notes": "Phenolic and tart.  The original yeast used to produce Wit in Belgium.",
            "best_for": "Belgian Wit",
            "max_reuse": 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Yeast.objects.count(), 1)
        self.assertEqual(Yeast.objects.get().name, 'Belgian Wit Ale')
        
        # fermentables
        url = '/fermentables/'
        data = {
            "type": "Grain",
            "name": "Pale Malt (2 Row) US",
            "raw_yield": "79.0000",
            "color": "2.0000",
            "origin": "US",
            "supplier": "",
            "notes": "Base malt for all beer styles",
            "coarse_fine_diff": "1.5000",
            "moisture": "4.0000",
            "diastatic_power": "140.0000",
            "protein": "12.3000",
            "max_in_batch": "100.0000",
            "recommend_mash": True,
            "ibu_gal_per_lb": "0.0000",
            "potential": "1.0363"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Fermentable.objects.count(), 1)
        self.assertEqual(Fermentable.objects.get().name, 'Pale Malt (2 Row) US')
        
        # waters
        url = '/waters/'
        data = {
            "name": "Dublin, Ireland",
            "calcium": "115.0000",
            "bicarbonate": "200.0000",
            "sulfate": "55.0000",
            "chloride": "19.0000",
            "sodium": "12.0000",
            "magnesium": "4.0000",
            "ph": "8.0000",
            "notes": "Irish ale water - used for dark, malty strong ales with medium bitterness.  Famous for dry stouts."
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Water.objects.count(), 1)
        self.assertEqual(Water.objects.get().name, 'Dublin, Ireland')
        
        
    def test_create_ingredient_malformed(self):
        url = '/hops/'
        data = {'type':'Bittering', 'form': 'Pellet', 'name': 'Cascade'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Hop.objects.count(), 0)
        
        
    def test_recipe_calculations(self):
        # Create the recipe
        
        
        # Check the OG, FG, Boil Volume, IBU, Color, Mash Efficiency, 
        
    