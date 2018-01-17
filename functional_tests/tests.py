from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.common.exceptions import (WebDriverException,
    NoSuchElementException)
from selenium.webdriver.common.keys import Keys

from dynamic_schemas.models import Schema, SchemaColumn, SchemaHelpUrl

import time

""" Possible extra test cases
    1. Check if correct instructions are passed to the table(Should maybe be a
    unittest).
    2. Change admin test to enter the site from desired entry point instead of
    /admin/
    3.
"""

MAX_WAIT = 10

class ToolKitMixin:
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
                if type_ == 'tag':
                    element = self.browser.find_element_by_tag_name(name)
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
                if type_ == 'css':
                    elements = self.browser.find_elements_by_css_selector(name)
                if type_ == 'tag':
                    elements = self.browser.find_elements_by_tag_name(name)
                return elements
            except(AssertionError, WebDriverException, NoSuchElementException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def login(self):
        username = self.wait_for_element('username', 'name')
        username.send_keys('test')

        # password = self.browser.find_element_by_name('password')
        password = self.wait_for_element('password', 'name')
        password.send_keys('testpw')

        password.send_keys(Keys.ENTER)



class SuperUserTest(ToolKitMixin, StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser.minimize_window()
        self.user = User.objects.create_superuser(
            'test', 'test@test.com', 'testpw'
            )

    def tearDown(self):
        self.browser.quit()

    def test_superuser_add_lock_delete_schema(self):
        """ This has become a very long test, should probably be cut down """
        # Superuser goes to the admin site.
        self.browser.get(self.live_server_url + '/admin/')

        # Superuser enters his username and password
        # username = self.browser.find_element_by_name('username')
        self.login()

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

        # He navigates back to the overview.
        self.wait_for_element('site-name', 'id')
        self.browser.find_element_by_tag_name('a').click()

        # He locates the Schema option.
        # He clicks on the Schemas option and gets sent the next page.
        # schema = self.wait_for_element('model-schema', 'class')
        # schema.find_element_by_tag_name('a').click()
        schema_help = self.wait_for_element('model-schema', 'class')
        schema_help.find_element_by_tag_name('a').click()

        # He locates the ADD SCHEMA + option, and clicks it
        self.wait_for_element('addlink', 'class').click()
        
        # He enters a name for the schema
        schema_name = self.wait_for_element('id_name', 'id')
        schema_name.send_keys('TestSchema')
        
        # Selects an instruction
        schema_instructs = self.wait_for_element('id_help_field_from', 'id')
        schema_option = schema_instructs.find_element_by_tag_name('option')
        schema_option.click()

        # Adds it to chosen field
        self.wait_for_element('id_help_field_add_link', 'id').click()

        # The Schema needs to be active.
        schema_active = self.wait_for_element('id_is_active', 'id').click()

        add_row = self.wait_for_element('add-row', 'class')
        add_row = add_row.find_element_by_tag_name('a').click
        # He creates a column for each possible combination. 
        # ()
        add_row()
        text_input1 = self.wait_for_element('id_schemacolumn_set-0-text', 'id')
        text_input1.send_keys('TESTING0')

        # Adds another row is_bool, 
        add_row()
        text_input2 = self.wait_for_element('id_schemacolumn_set-1-text', 'id')
        text_input2.send_keys('TESTING1')
        self.wait_for_element('id_schemacolumn_set-1-is_bool', 'id').click()

        # Another row is_editable
        add_row()
        text_input3 = self.wait_for_element('id_schemacolumn_set-2-text', 'id')
        text_input3.send_keys('TESTING2')
        self.wait_for_element('id_schemacolumn_set-2-is_editable', 'id').click()
        
        # another row is_editable_once, is_bool
        add_row()
        text_input4 = self.wait_for_element('id_schemacolumn_set-3-text', 'id')
        text_input4.send_keys('TESTING3')
        self.wait_for_element('id_schemacolumn_set-3-is_editable', 'id').click()
        self.wait_for_element('id_schemacolumn_set-3-is_bool', 'id').click()

        # SAVES THE TABLE
        self.wait_for_element('_save', 'name').click()

        # Checks if the table is showing correctly in Admin interface.
        # Gonna only check for name to prove that object exists.
        first_row = self.wait_for_element('field-name', 'class')
        row_name = first_row.find_element_by_tag_name('a')
        self.assertEqual('TestSchema', row_name.text)

        # Clicks the newly created table, and finds LOCK and clicks it. Then
        # saves table again.
        row_name.click()
        self.wait_for_element('id_is_locked', 'id').click()

        self.wait_for_element('_continue', 'name').click()

        # He then tries to delete a column, and change the name of another
        # column, which will result in SchemaIsLockedError.
        text_input1 = self.wait_for_element('id_schemacolumn_set-0-text', 'id')
        text_input1.send_keys('EXTRA')
        delete_input2 = self.browser.find_element_by_id('id_schemacolumn_set-1-DELETE')
        self.wait_for_element('_continue', 'name').click()

        ERROR_MSG = self.wait_for_element('body', 'tag')
        # __import__('ipdb').set_trace()
        self.assertEqual(ERROR_MSG.text, 'Server Error (500)')

        # Go back to admin, and delete table.
        self.browser.get(self.live_server_url + '/admin/dynamic_schemas/schema/')
        self.wait_for_element('action-select', 'class').click()
        
        action_dd = self.wait_for_element('action', 'name')
        action_dd_delete = action_dd.find_elements_by_tag_name('option')[1]
        action_dd_go = self.wait_for_element('index', 'name')
        action_dd.click()
        action_dd_delete.click()
        action_dd_go.click()

        # Site asks if he is sure, which he is. This will delete all columns
        # also even though schemaislocked. 
        inputs = self.wait_for_elements('input', 'tag')
        inputs[len(inputs) - 1].click()

        # Table should not exist at this point, assert if it does.
        # Replacement of expectedFailure.
        try:
            self.browser.find_element_by_tag_name('table')
        except NoSuchElementException:
            pass

        # admin logs out
        self.browser.get(self.live_server_url + '/admin/logout/')


class NewVisitorTest(ToolKitMixin, StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.user = User.objects.create_user(
            'test', 'test@test.com', 'testpw'
            )
        url = SchemaHelpUrl.objects.create(
            url='1234', name='1234', help_text='1234'
            )
        self.schema = Schema.objects.create(
            name='TEST', is_active=True
            )
        self.schema.help_field.add(url)
        self.schema.save()

        # Create every combination of columns
        SchemaColumn.objects.bulk_create([
            SchemaColumn(
                schema=self.schema, text='c1'
                ),
            SchemaColumn(
                schema=self.schema, text='c2', is_bool=True,
                ),
            SchemaColumn(
                schema=self.schema, text='c3', is_editable=True
                ),
            SchemaColumn(
                schema=self.schema, text='c4', is_bool=True, is_editable=True
                ),
            ])

        self.browser.get(self.live_server_url + '/rengoering/')
        self.login()

    def tearDown(self):
        self.logout()
        self.browser.quit()

    def logout(self):
        self.wait_for_element('glyphicon-log-out', 'class').click()

    def test_user_sees_right_index(self):
        self.schema_inv = Schema.objects.create(
            name='INVISIBLE', is_active=False
            )

        menu = self.wait_for_element('custom-btn-group', 'class')
        menu_btns = menu.find_elements_by_css_selector('#menu-btn')

        # Length of menu_btns should be 1, since INVISIBLE is inactive
        self.assertEqual(len(menu_btns), 1)
        self.assertNotIn('INVISIBLE', [b.text for b in menu_btns])
        self.assertIn('TEST', [b.text for b in menu_btns])

    def test_user_makes_first_entry_and_update(self):
        menu = self.wait_for_element('custom-btn-group', 'class')
        menu_btns = menu.find_elements_by_css_selector('#menu-btn')[0].click()

        new_entry = self.wait_for_element('btn', 'class')
        new_entry.click()

        form_box = self.wait_for_element('form-box', 'class')
        input1 = self.wait_for_element('id_c1', 'id')
        input1.send_keys('Initial')

        self.wait_for_element('submit-btn', 'class').click()

        # Check if in table
        table_data = self.wait_for_elements('td', 'tag')
        self.assertIn('Initial', [d.text for d in table_data])

        # Check if updatable
        first_row = self.wait_for_element('odd', 'class')
        first_row.click()

        update_btn = self.wait_for_element('buttons-selected', 'class')
        update_btn.click()

        c3 = self.wait_for_element('id_c3', 'id')
        c4 = self.wait_for_element('id_c4', 'id')

        c3.send_keys('UPDATEC3')

        c4.click()
        c4.send_keys('j')
        c4.send_keys(Keys.ENTER)

        c3.send_keys(Keys.ENTER)

        # Refetch tabledata element, and assert if our update is in
        table_row = self.wait_for_element('odd', 'class')
        table_data = self.wait_for_elements('td', 'tag')
        # __import__('ipdb').set_trace()
        table_data_list = [d.text for d in table_data]
        self.assertIn('Ja', table_data_list)
        self.assertIn('UPDATEC3', table_data_list)
        # Just making sure this is still in the list
        self.assertIn('Initial', table_data_list)

        #This concludes general use of the tables.

