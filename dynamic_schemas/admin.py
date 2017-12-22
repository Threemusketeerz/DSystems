from django import forms
from django.contrib import admin

from .models import Schema, SchemaQuestion, SchemaHelpUrl

# Register your models here.
class SchemaAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # We want default behavior, so calling __init__ first to fetch attrs
        super().__init__(*args, **kwargs) 

        # Edit the current instance's state to locked, by disabling access to
        # 'is_locked' attr. This can be accessed through python shell though as
        # an intended backdoor.
        # __import__('ipdb').set_trace()
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
            'fields': ('text',),
            }
        ),
        (None, {
            'classes': ('radio',),
            'fields': ('is_response_bool', 'is_editable',),
            }
        ),
    ]
    model = SchemaQuestion
    extra = 0

class MultipleChoiceInline(admin.StackedInline):
    fieldsets = [
        (None, {
            'fields': ('name')
            }
        )
    ]

class SchemaAdmin(admin.ModelAdmin):
    form = SchemaAdminForm
    save_on_top = True
    list_display = ('name', 'is_active', 'is_locked')
    list_filter = ('is_active', 'is_locked')
    fieldsets = [
        (None, {'fields': ['name', 'help_field', 'is_active', 'is_locked']}),
    ]
    inlines = [QuestionInline]


admin.site.register(Schema, SchemaAdmin)
admin.site.register(SchemaHelpUrl)
