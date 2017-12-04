from django.contrib import admin
from .models import Schema, SchemaQuestion, SchemaHelpUrl

# Register your models here.


class QuestionInline(admin.StackedInline):
    model = SchemaQuestion
    extra = 1


class SchemaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'help_field']}),
    ]
    inlines = [QuestionInline]


admin.site.register(Schema, SchemaAdmin)
admin.site.register(SchemaHelpUrl)
