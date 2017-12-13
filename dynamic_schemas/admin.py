from django import forms
from django.contrib import admin

from .models import Schema, SchemaQuestion, SchemaHelpUrl

# Register your models here.
class SchemaAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        # __import__('ipdb').set_trace()
        if kwargs['instance'].is_locked:
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
