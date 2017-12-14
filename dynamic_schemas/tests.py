from django.test import TestCase, Client, RequestFactory
from django.db import IntegrityError 
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist

from . import views
from .forms import SchemaResponseForm, ResponseUpdateForm
from .models import Schema, SchemaQuestion, SchemaResponse
from .exceptions import SchemaIsLockedError

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
        self.q1 = SchemaQuestion.objects.create(
                    schema=self.schema, 
                    text='test q1',
                    )

    def test_uniqueness_of_questions_by_schema_IntegrityError_True(self):
        with self.assertRaises(IntegrityError):
            q2 = SchemaQuestion.objects.create(
                    schema=self.schema,
                    text='test q1',
                    )

    @unittest.expectedFailure
    def test_uniqueness_of_questions_by_schema_IntegrityError_False(self):
        with self.assertRaises(IntegrityError):
            q2 = SchemaQuestion.objects.create(
                    schema=self.schema,
                    text='test q2',
                    )


class SchemaQuestionSaveTests(TestCase):
    def setUp(self):
        self.schema = Schema.objects.create(name='test schema', is_locked=True)

    def test_failure_at_save_if_schema_is_locked(self):
        with self.assertRaises(SchemaIsLockedError):
            SchemaQuestion.objects.create(
                    schema=self.schema, 
                    text='failing question',
                    )

    # --------------------------------------------------------------
    # These two tests provide proof that there is a backdoor to change schemas
    # if it is ABSOLUTELY necessary, otherwise it should be avoided.
    def test_schema_state_is_false(self):
        self.assertEqual(self.schema.is_active, False)
        self.assertEqual(self.schema.is_locked, True)

    def test_schema_can_still_save(self):
        self.schema.is_active = True 
        self.schema.is_locked = False
        self.schema.save
        self.assertEqual(self.schema.is_active, True)
        self.assertEqual(self.schema.is_locked, False)
    # --------------------------------------------------------------


class SchemaQuestionDeleteTests(TestCase):
    def setUp(self):
        self.schema = Schema.objects.create(name='test schema')
        self.q1 = SchemaQuestion.objects.create(schema=self.schema, text='q1')
        self.schema.is_locked = True
        self.schema.save()

    def test_failure_to_delete_if_schema_is_locked(self):
        with self.assertRaises(SchemaIsLockedError):
            SchemaQuestion.objects.get(pk=self.q1.id).delete()



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

    # def test_update_form_if_update_error_when_wrong_data(self):

        # form = ResponseUpdateForm(self.response, self.schema.id)
        # wrong_json = {'cyka': 'blyat', 'idi': 'nahoi', 
                # 'schema': self.schema.name}
        # r_url = f'/dynamic_schemas/{self.schema.id}/{self.response.id}/update/'
        # cli = self.client

        # with self.assertRaises(AttributeError):
            # cli_post = cli.post(r_url, data=wrong_json)
        
        # self.assertEqual(self.response.qa_set, self.json)

    # This seems like it belongs in views tests.
    def test_update_form_correct_data(self):
        form = ResponseUpdateForm(self.response, self.schema.id)
        r_url = reverse('dynamic_schemas:update_response',
                kwargs={'pk': self.schema.id, 'r_pk': self.response.id})

        updated_json = self.json
        updated_json[self.qe.text] = 'updated motherfucka'
        updated_json['schema'] = self.schema.name

        cli = self.client
        cli_post = cli.post(r_url, data=updated_json)

        cleaned_json = updated_json
        del cleaned_json['schema']

        self.assertEqual(self.response.qa_set, cleaned_json)


""" VIEWS TESTS """
class ViewTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_index_status_code_return_200(self):
        url = reverse('dynamic_schemas:schema_list')
        c_get = self.c.get(url)
        self.assertEqual(c_get.status_code, 200)

    def test_no_schema_returns_ObjectDoesNotExist(self):
        url = reverse('dynamic_schemas:schema_view', kwargs={'pk': 1})
        with self.assertRaises(ObjectDoesNotExist):
            self.c.get(url)

    def test_schema_returns_200(self):
        Schema.objects.create(name='test')
        url = reverse('dynamic_schemas:schema_view', kwargs={'pk': 1})
        self.assertEqual(self.c.get(url).status_code, 200)
        self.assertNotEqual(self.c.get(url).status_code, 404)

    def test_schema_row_create_returns_200(self):
        schema = Schema.objects.create(name='test')
        schema_q = SchemaQuestion.objects.create(text='q1', schema=schema)
        url = reverse('dynamic_schemas:create_form',
                kwargs={'pk': schema.id})
        self.assertEqual(self.c.get(url).status_code, 200)
        self.assertNotEqual(self.c.get(url).status_code, 404)
    
    def test_schema_row_update_returns_200(self):
        schema = Schema.objects.create(name='test')
        schema_q = SchemaQuestion.objects.create(text='q1', schema=schema)
        schema_r = SchemaResponse.objects.create(
                schema=schema, 
                qa_set={'q1': 'blabla'},
                )
        url = reverse(
                'dynamic_schemas:update_response',
                kwargs={'pk': schema.id, 'r_pk': schema_r.id},
                )
        self.assertEqual(self.c.get(url).status_code, 200)
        self.assertNotEqual(self.c.get(url).status_code, 404)

    
    def test_SchemaView_make_date_readable_returns_readable(self):
        # TODO Create global time format. In settings preferably.
        schema = Schema.objects.create(name='test')
        schema_q = SchemaQuestion.objects.create(text='q1', schema=schema)
        schema_r = SchemaResponse.objects.create(schema=schema, 
                qa_set={'q1': 'blabla'})
        url = reverse('dynamic_schemas:schema_view', kwargs={'pk': 1})

        request = self.factory.get(url)
        response = views.SchemaView.as_view()(request, 1)

        # Fetch date after .make_date_readable.
        readable_date = response.data.pop('all_responses')[0]['pub_date']

        # Date directly from db, used for table creation.
        unreadable_date = response.data.pop('single_response')['pub_date']

        self.assertNotEqual(readable_date, unreadable_date)

