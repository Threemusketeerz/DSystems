from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Schema, SchemaColumn, SchemaResponse, SchemaUrl


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
        self.schema_columns = schema.schemacolumn_set.all()
        
        self.URLS = self.schema.help_field.values_list('id', 'name')
        # import ipdb; ipdb.set_trace()
        # self.schema_urls = schema.schemaurl_set.all()
        # import ipdb; ipdb.set_trace()
        for column in self.schema_columns:
            if column.is_bool and column.is_editable_once:
                self.fields[column.text] = forms.ChoiceField(
                    choices=SELECT_CHOICES_EDIT,
                    widget=forms.Select(
                        attrs={'class': 'form-control'}
                        )
                    )
            elif column.is_bool and not column.is_editable_once:
                self.fields[column.text] = forms.ChoiceField(
                    choices=SELECT_CHOICES,
                    widget=forms.Select(
                        attrs={'class': 'form-control'}
                        )
                    )
            else:
                self.fields[column.text] = forms.CharField(
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
            instr_inst = get_object_or_404(SchemaUrl, pk=instr_id)

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
    
        for column, answer in instance.qa_set.items():
            queried_column = SchemaColumn.objects.get(schema=self.schema,
                                                   text=column)

            # If is_bool, we don't want it to be editable untill
            # proper conditions have been setup for such a scenario.
            if queried_column.is_bool:
                if queried_column.is_editable_once \
                and answer == SELECT_CHOICES_EDIT[0][0]:
                    # SELECT_CHOICES_EDIT[0][0] first tuple, first value
                    self.fields[column] = forms.ChoiceField(
                        choices=SELECT_CHOICES_EDIT,
                        widget=self.c_widget
                        )
                    self.fields[column].widget.attrs['disabled'] = False

                else:
                    self.fields[column] = forms.CharField(
                        initial=answer, 
                        widget=forms.TextInput(
                            attrs={'class': 'form-control', 'disabled': True}
                            )
                        )

            elif not queried_column.is_editable_once or answer != '':
                self.fields[column] = forms.CharField(
                    required=False,
                    max_length=100,
                    initial=answer,
                    widget=forms.TextInput(
                        attrs={'class':'form-control', 'disabled': True}
                        )
                    )
                
            else:
                self.fields[column] = forms.CharField(
                    required=False,
                    max_length=100,
                    initial=answer, # Should be empty '' else remove this field
                    widget=forms.TextInput(
                        attrs={'class': 'form-control'}
                        )
                    )

    def is_valid(self):
        # Parent validation first, get cleaned data.
        """ Cleans own data, makes sure columns is editable and is empty """
        editable_columns = { 
            c.text:
            c.is_editable_once for c in self.schema_columns
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
