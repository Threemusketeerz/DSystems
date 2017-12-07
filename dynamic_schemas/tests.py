from django.test import TestCase

from .models import Schema, SchemaQuestion, SchemaResponse
from .forms import SchemaResponseForm, ResponseUpdateForm

import unittest

# Create your tests here.

def create_json_for_response(q_instances, response):
    json = {}
    for i, q in enumerate(q_instances):
        json[q.text] = response + f' {i}'

    return json

class SchemResponseTest(TestCase):
    def setUp(self):
        self.schema = Schema.objects.create(name='test schema')
        self.q1 = SchemaQuestion.objects.create(schema=self.schema, text='test q1')
        self.q2 = SchemaQuestion.objects.create(schema=self.schema, text='test q2')
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

    def test_response_form_booleanfield(self):
        form = SchemaResponseForm(self.schema)

        self.assertNotEqual(str(form.fields[self.qb.text].__class__), 
                         "<class 'django.forms.fields.CharField'>")
        self.assertEqual(str(form.fields[self.qb.text].__class__),
                         "<class 'django.forms.fields.BooleanField'>")


class ResponseFormUpdateTest(TestCase):
    pass
