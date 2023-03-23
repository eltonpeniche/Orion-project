import time

from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class OrionBaseFunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)

class OrionHomePageFunctionalTest(OrionBaseFunctionalTest):
    
    def test_the_test(self):
        self.browser
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME,  'body')
        self.assertIn('Entre com o seu Login e Senha', body.text)
      