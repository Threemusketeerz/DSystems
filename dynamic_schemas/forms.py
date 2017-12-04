from django import forms
from django.core.exceptions import ValidationError

from .models import Schema, SchemaQuestion, SchemaResponse


class SchemaResponseForm(forms.Form):

    def __init__(self, schema, *args, **kwargs):
        super().__init__(*args, **kwargs)
        schema_questions = schema.schemaquestion_set.all()
        self.schema = schema
        for question in schema_questions:
            if question.is_response_bool:
                self.fields[question.text]=forms.BooleanField(
                    required=False,
                    widget=forms.TextInput(
                        attrs={'class':'form-control'}
                    ),
                )

            else:
                self.fields[question.text] = forms.CharField(
                    max_length=200,
                    required=False,
                    empty_value='',
                    widget=forms.TextInput(
                        attrs={'class':'form-control'}
                    ),
                )

        self.fields['schema'] = forms.CharField(
            initial=schema.name,
            widget=forms.HiddenInput(),
            required=True
        )

    def save(self, commit=True, *args, **kwargs):
        if self.cleaned_data:
            # We remove the schema from the dict itself, it gets passed to
            # schema attr on object instead

            SchemaResponse.objects.create(
                schema = self.schema,
                qa_set = self.cleaned_data,
            )

        else:
            return ValidationError("NOT VALID")


    def is_consistent(self):
        # This is sort of a wrapper for is_valid to make the data valid to us.
        # This will fill out the cleaned_data, if it didn't submit a question. It
        # is a catcher of consistency.
        # There will be complications if a new question is added to the Schema.
        # This should either be avoided or built into the function.

        q_set = SchemaQuestion.objects.filter(schema=self.schema)
        q_set_list = [q.text for q in q_set]

        # This should honestly probably be moved to VIEWS.
        if self.is_valid():

            del self.cleaned_data['schema']

            qa_set_keys = [ k for k in self.cleaned_data.keys() ]

            print('Comparing: ', q_set_list)
            print('With: ', qa_set_keys)

            if qa_set_keys == q_set_list:
                return print('Lists are consistent')

            else:
                for q in q_set_list:
                    if q in qa_set_keys:
                        continue
                    else:
                        print(f'{q} is not in form; Replacing with empty answer')
                        qa_set[q] = ''

        else:
            return ValidationError('Form is not valid')
        return True
