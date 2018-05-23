import json
from django.test import TestCase
from food.models import Categorie
from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from food.utils import get_product, get_result

class CategorieTestCase(TestCase):
    """ Categorie database """
    def setUp(self):
        Categorie.objects.create(categorie_name='TestName', categorie_url='http://test.com')
    
    def test_categorie_insertion(self):
        """ Categorie can insert a line """
        testName = Categorie.objects.get(categorie_name='TestName')
        self.assertEqual(testName.categorie_url, 'http://test.com')

class UrlTestCase(TestCase):
    """ URL """
    def setUp(self):
        self.client = Client()

    def test_url(self):
        """ Url test with visitor client """
        home = self.client.get('')
        result = self.client.get('/result/test')
        resultFalse = self.client.get('/result/')
        product = self.client.get('/product/1')
        account = self.client.get('/account/')
        connexion = self.client.get('/connexion/')
        deconnexion = self.client.get('/deconnexion/')
        subscribe = self.client.get('/subscribe/')

        self.assertEqual(home.status_code, 200)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(resultFalse.status_code, 404)
        self.assertEqual(product.status_code, 302)
        self.assertEqual(account.status_code, 302)
        self.assertEqual(connexion.status_code, 200)
        self.assertEqual(deconnexion.status_code, 302)
        self.assertEqual(subscribe.status_code, 200)


class MySeleniumTests(StaticLiveServerTestCase):
    """ Try connexion and logout of a user """
    fixtures = ['user.json']
    from selenium.webdriver.support.wait import WebDriverWait
    timeout = 2

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, '/connexion/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('Paul')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('azerty')
        self.selenium.find_element_by_xpath('//input[@value="Se connecter"]').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('carrot'))
        self.selenium.find_element_by_xpath('//a[@title="Déconnexion"]').click()

class OffTestCase(TestCase):
    """ Test the OpenFoodFacts request """
    fixtures = ['categorie.json']

    def setUp(self):
        Categorie.objects.create(
            categorie_name='Petit-déjeuners', categorie_url='https://fr.openfoodfacts.org/categorie/petit-dejeuners')

    def test_get_product(self):
        """ Get_product test """
        request = get_product('Nutella')
        result = [['Petit-déjeuners', 'Produits à tartiner', 'Produits à tartiner sucrés',
                    'Pâtes à tartiner', 'Pâtes à tartiner au chocolat',
                    'Pâtes à tartiner aux noisettes', 'Pâtes à tartiner aux noisettes et au cacao'], ['e'], 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.400.jpg']
        self.assertEqual(request, result )

    def test_get_product_is_none(self):
        """ Return None """
        request = get_product('ThisProductDoesntExist')
        self.assertEqual(request, None)

    def test_get_result(self):
        """ Get_result test """
        categorie = ['Petit-déjeuners', 'Produits à tartiner', 'Produits à tartiner sucrés',
                     'Pâtes à tartiner', 'Pâtes à tartiner au chocolat',
                     'Pâtes à tartiner aux noisettes']
        nutrition_grade =  ['e']

        result = get_result(categorie, nutrition_grade)
        self.assertIs(type(result), str)

