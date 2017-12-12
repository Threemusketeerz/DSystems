from django.contrib import admin
from .models import Schema, SchemaQuestion, SchemaHelpUrl

# Register your models here.


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
    extra = 1


class SchemaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'is_active',)
    list_filter = ('is_active',)
    fieldsets = [
        (None, {'fields': ['name', 'help_field', 'is_active']}),
    ]
    inlines = [QuestionInline]


admin.site.register(Schema, SchemaAdmin)
admin.site.register(SchemaHelpUrl)
