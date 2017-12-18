from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField

from .exceptions import SchemaIsLockedError
# Create your models here.


class SchemaHelpUrl(models.Model):

    """This will be initialized above all the fields. Beneath the header. this
    will contain urls referencing links connected to the schema."""

    url = models.URLField()
    link_name = models.CharField(max_length=50,)
    help_text = models.TextField(default='',)

    def __str__(self):
        return self.link_name


class Schema(models.Model):

    """The mothership for filtering the correct tables"""

    name = models.CharField(max_length=100,)

    help_field = models.ManyToManyField(SchemaHelpUrl,
                                        verbose_name='Instruktions felt',)
    is_active = models.BooleanField(default=False,
                                    verbose_name='Aktivt',)
    is_locked = models.BooleanField(default=False,
                                    verbose_name='Lås',
                                    help_text='Hvis du låser kan du ikke ændre'
                                    ' tabellen i fremtiden.')

    def __str__(self):
        return self.name


class SchemaQuestion(models.Model):

    """Question for schema"""

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,)
    text = models.CharField(max_length=100,)
    is_response_bool = models.BooleanField(default=False,
                                           verbose_name='Ja/Nej spørgsmål',)
    is_editable = models.BooleanField(default=False,
                                      verbose_name='Felt kan ændres',)

    class Meta:
        unique_together = ('schema', 'text',)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.schema.is_locked:
            raise SchemaIsLockedError(f'{self.schema.name}.is_locked = '
                                      f'{self.schema.is_locked}, can\'t save')
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.schema.is_locked:
            raise SchemaIsLockedError(f'{self.schema.name}.is_locked = '
                                      f'{self.schema.is_locked}, can\'t delete')
        else:
            super().delete(*args, **kwargs)


class SchemaResponse(models.Model):

    """Response to question set"""

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=1) # admin

    qa_set = JSONField()

    pub_date = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return f'{self.id}'

    def get_questions(self):
        return SchemaQuestion.objects.filter(schema=self.schema)


