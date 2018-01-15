from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        browser = webdriver.Firefox()
        browser.get(self.live_server_url)

    def tearDown(self):
        browser.quit()
