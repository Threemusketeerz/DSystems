from django import forms
from django.core.exceptions import ValidationError

from .models import Schema, SchemaQuestion, SchemaResponse


# Rename ResponseForm
class SchemaResponseForm(forms.Form):

    def __init__(self, schema, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_questions = schema.schemaquestion_set.all()
        self.schema = schema
        for question in self.schema_questions:
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
        # This assumes .is_valid is checked first.
        if self.cleaned_data:
            # We remove the schema from the dict itself, it gets passed to
            # schema attr on object instead

            SchemaResponse.objects.create(
                schema = self.schema,
                qa_set = self.cleaned_data,
            )

        else:
            return ValidationError("NOT VALID")


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
        # self.pk = pk
    
        for q, a in instance.qa_set.items():
            queried_q = SchemaQuestion.objects.get(schema=self.schema, text=q)

            # If is_response_bool, we don't want it to be editable untill
            # proper conditions have been setup for such a scenario.
            if queried_q.is_response_bool:
                self.fields[q] = forms.BooleanField(
                    required=False,
                    widget=forms.TextInput(
                        attrs={'class':'form-control', 'readonly': True}
                    )
                )
                # __import__('ipdb').set_trace()


            # If it is editable, and NOT empty. After it has been entered we
            # dont want people to enter new data.
            elif not queried_q.is_editable or a != '':
                self.fields[q] = forms.CharField(
                    required=False,
                    max_length=100,
                    initial=a,
                    widget=forms.TextInput(
                        attrs={'class':'form-control', 'readonly': True}
                    )
                )
                
            else:
                self.fields[q] = forms.CharField(
                    required=False,
                    max_length=100,
                    initial=a, # Should be empty '' else remove this field
                    widget=forms.TextInput(
                        attrs={'class': 'form-control'}
                    )
                )

        self.fields['schema'] = forms.CharField(
            initial=instance.schema.name,
            widget=forms.HiddenInput(),
            required=True
        )

    def is_valid(self):

        # Parent validation first, get cleaned data.
        valid = super().is_valid()

        if not valid:
            return valid
        # __import__('ipdb').set_trace()

        fetch_questions = [q.text for q in self.schema_questions]
        fetch_questions.append(self.schema.name)

        for q in self.cleaned_data:
            if q not in fetch_questions:
                try:
                    raise AttributeError(f'{q} is in your imagination')
                finally:
                    return False

        return True
        
        # questions = SchemaQuestion.objects.filter(schema=self.schema)

        # list_to_comp = [q for q in cleaned_data]
        # q_to_comp = [q.text for q in questions] 


    def update(self, *args, **kwargs):
        if self.cleaned_data:

            __import__('ipdb').set_trace()
            # Update instancewith new qa_set. 
            del self.cleaned_data['schema']

            self.instance.qa_set = self.cleaned_data 
            self.instance.save()

        else:
            return ValidationError("NOT VALID")
