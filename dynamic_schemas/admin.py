from django import forms
from django.forms import ModelMultipleChoiceField
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Schema, SchemaColumn, SchemaHelpUrl

# Register your models here.
class SchemaAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # We want default behavior, so calling __init__ first to fetch attrs
        super().__init__(*args, **kwargs) 

        # Edit the current instance's state to locked, by disabling access to
        # 'is_locked' attr. This can be accessed through python shell though as
        # an intended backdoor.
        if 'instance' in kwargs:
            if hasattr(kwargs['instance'], 'is_locked') \
            and kwargs['instance'].is_locked:
                self.fields['is_locked'].widget = forms.HiddenInput()
    
    class Meta:
        model = Schema
        fields = ('__all__')


class QuestionInline(admin.StackedInline):
    fieldsets = [         
        (None, {
            'fields': ('text', 'is_bool', 'is_editable',),
            }
        ),
    ]
    model = SchemaColumn
    extra = 0



class SchemaAdmin(admin.ModelAdmin):
    form = SchemaAdminForm
    save_on_top = True
    list_display = (
        'name', 'is_active', 'is_locked', 'date_created',
        'date_modified', 'date_obsolete',
        )

    list_filter = (
        'is_active', 'is_locked', 'date_created',
        'date_modified', 'date_obsolete',
        )

    fieldsets = [
        (None, {'fields': [
                'name', 'help_field', 'is_active', 'is_locked', 
                'is_obsolete',
                ]
            }
        ),
    ]
    filter_horizontal = ('help_field',)

    inlines = [QuestionInline]

admin.site.site_url = '/rengoering/'
admin.site.site_header = 'Damino Systems'

admin.site.register(Schema, SchemaAdmin)
admin.site.register(SchemaHelpUrl)
