from django.test import TestCase, Client
from django.db import IntegrityError

from .models import Schema, SchemaQuestion, SchemaResponse
from .forms import SchemaResponseForm, ResponseUpdateForm

import unittest
import random

# Create your tests here.


""" HELPER FUNCTIONS """
def create_json_for_response(q_instances, response):
    json = {}
    for i, q in enumerate(q_instances):
        if q.is_response_bool:
            json[q.text] = bool(random.getrandbits(1))
        elif q.is_editable:
            json[q.text] = ''
        else:
            json[q.text] = response + f' {i}'

    return json


""" MODEL TESTS """
class SchemaQuestionTests(TestCase):
    def setUp(self):
        self.schema = Schema.objects.create(name='test schema')
        self.q1 = SchemaQuestion.objects.create(schema=self.schema, 
                text='test q1')

    def test_uniqueness_of_questions_by_schema_IntegrityError_True(self):
        with self.assertRaises(IntegrityError):
            q2 = SchemaQuestion.objects.create(schema=self.schema,
                    text='test q1')

    @unittest.expectedFailure
    def test_uniqueness_of_questions_by_schema_IntegrityError_False(self):
        with self.assertRaises(IntegrityError):
            q2 = SchemaQuestion.objects.create(schema=self.schema,
                    text='test q2')



""" FORM TESTS """
class SchemaResponseTest(TestCase):
    def setUp(self):
        self.schema = Schema.objects.create(name='test schema')
        self.q1 = SchemaQuestion.objects.create(schema=self.schema, 
                text='test q1')
        self.q2 = SchemaQuestion.objects.create(schema=self.schema,
                text='test q2')
        self.questions = SchemaQuestion.objects.filter(schema=self.schema)
        
    def test_get_questions_set_is_equal(self):
        json = create_json_for_response(self.questions, 'cool')
        SchemaResponse.objects.create(schema=self.schema,qa_set=json)
        r = SchemaResponse.objects.filter(schema=self.schema).first()

        self.assertSetEqual(r.get_questions(), self.questions)

    @unittest.expectedFailure
    def test_get_questions_set_not_equal(self):
        json = create_json_for_response(self.questions, 'cool')
        SchemaResponse.objects.create(schema=self.schema,qa_set=json)
        r = SchemaResponse.objects.filter(schema=self.schema).first()
        
        self.assertSetEqual(r.get_questions(), 'blabla')
    

class FormTests(TestCase):
    def setUp(self):
        self.schema = Schema.objects.create(name='test schema')
        self.q1 = SchemaQuestion.objects.create(schema=self.schema, text='test q1')
        self.q2 = SchemaQuestion.objects.create(schema=self.schema, text='test q2')
        self.qb = SchemaQuestion.objects.create(schema=self.schema, 
                text='test qb',
                is_response_bool=True
                )
        self.questions = SchemaQuestion.objects.filter(schema=self.schema)

    def test_response_form_correct_field_len(self):
        json = create_json_for_response(self.questions, 'forms')
        SchemaResponse.objects.create(schema=self.schema,qa_set=json)
        # r = SchemaResponse.objects.filter(schema=schema).first()
        form = SchemaResponseForm(self.schema)
        form_fields_len = len(form.fields)
        expected_len = len(self.questions) + 1

        self.assertEqual(form_fields_len, expected_len)
        self.assertNotEquals(form_fields_len, form_fields_len -1)

    def test_response_form_fields_match_questions_plus_schema(self):
        json = create_json_for_response(self.questions, 'forms')

        form = SchemaResponseForm(self.schema)

        # Since fields are attributes, we're expecting it to look like this
        # ['test q1', 'test q2', 'schema']
        form_fields = [f for f in form.fields]
        exp_fields = [q.text for q in self.questions]
        exp_fields.append('schema')

        self.assertEqual(form_fields, exp_fields)


    def test_response_data_is_valid(self):
        data = {self.q1.text: 'a1', self.q2.text: 'a2', 
                'schema': self.schema.name} 

        form = SchemaResponseForm(self.schema, data)

        self.assertEqual(form.is_valid(), True)

    
    def test_response_form_charfield(self):
    
        form = SchemaResponseForm(self.schema)

        self.assertEqual(str(form.fields[self.q1.text].__class__), 
                         "<class 'django.forms.fields.CharField'>")
        self.assertNotEqual(str(form.fields[self.q1.text].__class__),
                         "<class 'django.forms.fields.BooleanField'>")

    def test_response_form_if_booleanfield_is_charfield(self):
        form = SchemaResponseForm(self.schema)

        self.assertNotEqual(str(form.fields[self.qb.text].__class__), 
                         "<class 'django.forms.fields.CharField'>")

    def test_response_form_if_booleanfield_is_booleanfield(self):
        form = SchemaResponseForm(self.schema)
        self.assertEqual(str(form.fields[self.qb.text].__class__),
                         "<class 'django.forms.fields.BooleanField'>")

class ResponseFormUpdateTests(TestCase):

    def setUp(self):
        self.schema = Schema.objects.create(name='test schema')
        self.q1 = SchemaQuestion.objects.create(schema=self.schema, 
                text='test q1')
        self.q2 = SchemaQuestion.objects.create(schema=self.schema, 
                text='test q2')
        self.qb = SchemaQuestion.objects.create(schema=self.schema, 
                text='test qb',
                is_response_bool=True
                )
        self.qe = SchemaQuestion.objects.create(schema=self.schema, 
                text='test qe', 
                is_editable=True)

        self.questions = SchemaQuestion.objects.filter(schema=self.schema)

        self.json = create_json_for_response(self.questions, 'form_update')

        self.response = SchemaResponse.objects.create(schema=self.schema,
                qa_set=self.json)

        self.client = Client()

    def test_update_form_if_booleanfield_is_charfield(self):
        form = ResponseUpdateForm(self.response, self.schema.id)

        self.assertNotEqual(str(form.fields[self.qb.text].__class__), 
                         "<class 'django.forms.fields.CharField'>")

    def test_update_form_if_booleanfield_is_booleanfield(self):
        form = ResponseUpdateForm(self.response, pk=self.schema.id)
        self.assertEqual(str(form.fields[self.qb.text].__class__),
                         "<class 'django.forms.fields.BooleanField'>")

    def test_update_form_if_update_error_when_wrong_data(self):

        form = ResponseUpdateForm(self.response, self.schema.id)
        wrong_json = {'cyka': 'blyat', 'idi': 'nahoi', 
                'schema': self.schema.name}
        r_url = f'/dynamic_schemas/{self.schema.id}/{self.response.id}/update/'
        cli = self.client

        with self.assertRaises(AttributeError):
            cli_post = cli.post(r_url, data=wrong_json)
        
        # self.assertEqual(self.response.qa_set, self.json)


    def test_update_form_correct_data(self):
        form = ResponseUpdateForm(self.response, self.schema.id)
        r_url = f'/dynamic_schemas/{self.schema.id}/{self.response.id}/update/'

        updated_json = self.json
        updated_json[self.qe.text] = 'updated motherfucka'
        updated_json['schema'] = self.schema.name

        cli = self.client
        cli_post = cli.post(r_url, data=updated_json)

        cleaned_json = updated_json
        del cleaned_json['schema']

        self.assertEqual(self.response.qa_set, cleaned_json)

