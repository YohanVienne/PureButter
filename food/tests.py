from django.test import TestCase
from food.models import Categorie, Product
from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


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
        product = self.client.get('/product/test')
        account = self.client.get('/account/')
        connexion = self.client.get('/connexion/')
        deconnexion = self.client.get('/deconnexion/')
        subscribe = self.client.get('/subscribe/')

        self.assertEqual(home.status_code, 200)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(product.status_code, 200)
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
