from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Schema, SchemaQuestion, SchemaResponse


# Rename ResponseForm
SELECT_CHOICES = [ 
    ('Ingenting','Ingenting'),
    ('Ja','Ja'), 
    ('Nej','Nej'), 
]
SELECT_LEN = len(SELECT_CHOICES)

class SchemaResponseForm(forms.Form):

    def __init__(self, schema, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.schema_questions = schema.schemaquestion_set.all()
        self.schema = schema
        for question in self.schema_questions:
            if question.is_response_bool:
                    self.fields[question.text] = forms.ChoiceField(
                        choices=SELECT_CHOICES,
                        widget=forms.Select(
                            attrs={
                            'class': 'form-control'
                            }
                        )

                    )
                # self.fields[question.text]=forms.NullBooleanField(
                    # required=False,
                    # widget=forms.TextInput(
                        # attrs = {
                            # 'class':'form-check-input',
                            # 'type': 'checkbox',
                        # }
                    # ),
                # )

            else:
                self.fields[question.text] = forms.CharField(
                    max_length=200,
                    required=False,
                    empty_value='',
                    widget=forms.TextInput(
                        attrs={'class':'form-control'}
                    ),
                )

    def save(self, commit=True, *args, **kwargs):

        if self.cleaned_data:

            instance = SchemaResponse(
                schema = self.schema,
                qa_set = self.cleaned_data,
            )

            if commit:
                instance.save()

        return instance

        # else:
            # return ValidationError("NOT VALID")


class ResponseUpdateForm(forms.Form):

    """
    Handles the form for updating the fields.
    """
    
    def __init__(self, instance, pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # schema_questions = instance.get_questions
        # __import__('ipdb').set_trace()

        self.instance = instance 
        self.schema = Schema.objects.get(pk=pk)
        self.schema_questions = self.schema.schemaquestion_set.all()
        self.c_widget = forms.Select(
                            attrs={
                                'class': 'form-control'
                            }
                        )
        # self.pk = pk
    
        for qstn, ansr in instance.qa_set.items():
            queried_q = SchemaQuestion.objects.get(schema=self.schema,
                                                   text=qstn)

            # If is_response_bool, we don't want it to be editable untill
            # proper conditions have been setup for such a scenario.
            if queried_q.is_response_bool:
                if queried_q.is_editable \
                and ansr == 'Ingenting':
                    self.fields[qstn] = forms.ChoiceField(
                        choices=SELECT_CHOICES,
                        widget=self.c_widget
                        
                    )
                    self.fields[qstn].widget.attrs['readonly'] = False
                    # self.fields[q] = forms.NullBooleanField( # required=False,
                        # initial=a,
                        # widget=forms.TextInput(
                            # attrs={
                                # 'class':'form-check-input',
                                # 'type': 'checkbox',
                                # 'indeterminate': True,
                            # }
                        # )
                    # )

                else:
                    self.fields[qstn] = forms.ChoiceField(
                        choices=SELECT_CHOICES,
                        widget=self.c_widget
                    )
                    self.fields[qstn].widget.attrs['readonly'] = True
                    # self.fields[q].initial = a
                    # self.fields[q] = forms.NullBooleanField(
                        # required=False,
                        # widget=forms.TextInput(
                            # attrs={
                                # 'class':'form-check-input',
                                # 'type': 'checkbox',
                                # 'disabled': True,
                            # }
                        # )
                    # )
                    self.fields[qstn].initial = ansr

            elif not queried_q.is_editable or ansr != '':
                self.fields[qstn] = forms.CharField(
                    required=False,
                    max_length=100,
                    initial=ansr,
                    widget=forms.TextInput(
                        attrs={'class':'form-control', 'readonly': True}
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

        # self.fields['schema'] = forms.CharField(
            # initial=instance.schema.name,
            # widget=forms.HiddenInput(),
            # required=True
        # )

    def is_valid(self):

        # Parent validation first, get cleaned data.
        valid = super().is_valid()

        if not valid:
            return valid

        fetch_questions = [q.text for q in self.schema_questions]
        # fetch_questions.append(self.schema.name)

        # Keeping this for now, as long as it doesnt cause trouble
        for qstn in self.data:
            if qstn not in fetch_questions \
            and qstn != 'csrfmiddlewaretoken':
                try:
                    raise AttributeError(f'{qstn} is in your imagination')
                finally:
                    return False

        return True
        
        # questions = SchemaQuestion.objects.filter(schema=self.schema)

        # list_to_comp = [q for q in cleaned_data]
        # q_to_comp = [q.text for q in questions] 


    def update(self, *args, **kwargs):
        if self.cleaned_data:

            self.instance.qa_set = self.cleaned_data 
            self.instance.save()

        else:
            return ValidationError("NOT VALID")
