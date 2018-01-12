from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Schema, SchemaColumn, SchemaResponse, SchemaHelpUrl


# Rename ResponseForm
SELECT_CHOICES_EDIT = [ 
    ('------', '------'),
    ('Nej','Nej'), 
    ('Ja','Ja'), 
    ]
SELECT_CHOICES = [
    ('Nej', 'Nej'),
    ('Ja', 'Ja'),
    ]
SELECT_LEN = len(SELECT_CHOICES)


class SchemaResponseForm(forms.Form):

    def __init__(self, schema, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.schema = schema
        self.schema_questions = schema.schemacolumn_set.all()
        
        self.URLS = self.schema.help_field.values_list('id', 'name')
        # import ipdb; ipdb.set_trace()
        # self.schema_urls = schema.schemahelpurl_set.all()
        # import ipdb; ipdb.set_trace()
        for question in self.schema_questions:
            if question.is_bool and question.is_editable:
                self.fields[question.text] = forms.ChoiceField(
                    choices=SELECT_CHOICES_EDIT,
                    widget=forms.Select(
                        attrs={'class': 'form-control'}
                        )
                    )
            elif question.is_bool and not question.is_editable:
                self.fields[question.text] = forms.ChoiceField(
                    choices=SELECT_CHOICES,
                    widget=forms.Select(
                        attrs={'class': 'form-control'}
                        )
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

        self.fields['instruktion'] = forms.ChoiceField(
              choices=self.URLS,
              widget=forms.Select(
                  attrs={'class': 'form-control'}
                  )
              )

    def save(self, commit=True, *args, **kwargs):

        if self.cleaned_data:
            instr_id = self.cleaned_data.pop('instruktion')
            instr_inst = get_object_or_404(SchemaHelpUrl, pk=instr_id)

            instance = SchemaResponse(
                schema=self.schema,
                qa_set=self.cleaned_data,
                instruction=instr_inst,
                )

            if commit:
                instance.save()

        return instance


class ResponseUpdateForm(forms.Form):

    """
    Handles the form for updating the fields.
    """
    
    def __init__(self, instance, pk, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.instance = instance 
        self.schema = Schema.objects.get(pk=pk)
        self.schema_columns = self.schema.schemacolumn_set.all()
        self.c_widget = forms.Select(
            attrs={'class': 'form-control'},
            )
    
        for qstn, ansr in instance.qa_set.items():
            queried_q = SchemaColumn.objects.get(schema=self.schema,
                                                   text=qstn)

            # If is_bool, we don't want it to be editable untill
            # proper conditions have been setup for such a scenario.
            if queried_q.is_bool:
                if queried_q.is_editable \
                and ansr == SELECT_CHOICES_EDIT[0][0]:
                    # SELECT_CHOICES_EDIT[0][0] first tuple, first value
                    self.fields[qstn] = forms.ChoiceField(
                        choices=SELECT_CHOICES_EDIT,
                        widget=self.c_widget
                        )
                    self.fields[qstn].widget.attrs['disabled'] = False

                else:
                    self.fields[qstn] = forms.CharField(
                        initial=ansr, 
                        widget=forms.TextInput(
                            attrs={'class': 'form-control', 'disabled': True}
                            )
                        )

            elif not queried_q.is_editable or ansr != '':
                self.fields[qstn] = forms.CharField(
                    required=False,
                    max_length=100,
                    initial=ansr,
                    widget=forms.TextInput(
                        attrs={'class':'form-control', 'disabled': True}
                        )
                    )
                
            else:
                self.fields[qstn] = forms.CharField(
                    required=False,
                    max_length=100,
                    initial=ansr, # Should be empty '' else remove this field
                    widget=forms.TextInput(
                        attrs={'class': 'form-control'}
                        )
                    )

    def is_valid(self):
        # Parent validation first, get cleaned data.
        """ Cleans own data, makes sure columns is editable and is empty """
        editable_columns = { 
            c.text:
            c.is_editable for c in self.schema_columns
            }

        exists = {} 
        for key, value in self.data.items():
            if key in self.instance.qa_set \
            and editable_columns[key] \
            and (self.instance.qa_set[key] == '' \
            or self.instance.qa_set[key] == '------'):
                exists[key] = value

        if exists:
            self.cleaned_data = exists
            return True

        return False


    def update(self, *args, **kwargs):
        if self.cleaned_data:

            # __import__('ipdb').set_trace()
            for key, value in self.cleaned_data.items():
                self.instance.qa_set[key] = value
            self.instance.save()

        else:
            return ValidationError("NOT VALID")
