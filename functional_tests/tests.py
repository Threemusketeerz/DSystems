from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.common.exceptions import (WebDriverException,
    NoSuchElementException)
from selenium.webdriver.common.keys import Keys


import time

MAX_WAIT = 10

class SuperUserTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.user = User.objects.create_superuser(
            'test', 'test@test.com', 'testpw'
            )

    # def tearDown(self):
        # self.browser.quit()

    def wait_for_element(self, name, type_):
        start_time = time.time()
        while True:
            try:
                if type_ == 'name':
                    element = self.browser.find_element_by_name(name)
                if type_ == 'class':
                    element = self.browser.find_element_by_class_name(name)
                if type_ == 'id':
                    element = self.browser.find_element_by_id(name)
                return element
            except(AssertionError, WebDriverException, NoSuchElementException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_elements(self, name, type_):
        start_time = time.time()
        while True:
            try:
                if type_ == 'name':
                    elements = self.browser.find_elements_by_name(name)
                if type_ == 'class':
                    elements = self.browser.find_elements_by_class_name(name)
                if type_ == 'id':
                    elements = self.browser.find_elements_by_id(name)
                return elements
            except(AssertionError, WebDriverException, NoSuchElementException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
                

    def test_superuser_capabilities(self):
        # Superuser goes to the admin site.
        self.browser.get(self.live_server_url + '/admin/')

        # Superuser enters his username and password
        # username = self.browser.find_element_by_name('username')
        username = self.wait_for_element('username', 'name')
        username.send_keys('test')

        # password = self.browser.find_element_by_name('password')
        password = self.wait_for_element('password', 'name')
        password.send_keys('testpw')

        password.send_keys(Keys.ENTER)

        # Superuser now sees the screen with the admin options.
        # He wants to create a new Schema, so he can test out the front end
        # part of the page. But first he needs to create a help url, since the
        # design requires him to do so. He locates SchemaHelpUrls and clicks
        # it.
        schema_help = self.wait_for_element('model-schemahelpurl', 'class')
        schema_help.find_element_by_tag_name('a').click()

        # He will add a simple help url
        self.wait_for_element('addlink', 'class').click()

        # Input test text into fields.
        # Url is modified to CharField instead of URLField to avoid url
        # restrictions. Since we're on a local server. See
        # dynamic_schemas.models for more info.
        schema_help_url = self.wait_for_element('url','name')
        schema_help_url.send_keys('www.google.dk')

        schema_help_name = self.wait_for_element('name','name')
        schema_help_name.send_keys('test')
        
        schema_help_helptext = self.wait_for_element('help_text','name')
        schema_help_helptext.send_keys('link to www.google.dk')

        # He saves the new SchemaHelpUrl 
        self.wait_for_element('_save', 'name').click()

        # He locates the Schema option.
        # He clicks on the Schemas option and gets sent the next page.
        # schema = self.wait_for_element('model-schema', 'class')
        # schema.find_element_by_tag_name('a').click()

        # He locates the ADD SCHEMA + option, and clicks it
        # self.wait_for_element('addlink', 'class').click()
        
        # He enters a name for the schema
        

        # Creates an instruction to use

        # The Schema needs to be active.

        # He creates a column for each possible combination. 
        # (is_editable_once), (is_editable_once, is_bool), ()

        self.fail('Finish the test')

