from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from jsonfield import JSONField

from .exceptions import SchemaIsLockedError
# Create your models here.


class SchemaHelpUrl(models.Model):

    """This will be initialized above all the fields. Beneath the header. this
    will contain urls referencing links connected to the schema."""

    url = models.CharField(max_length=200)
    name = models.CharField(max_length=50,)
    help_text = models.TextField(default='',)

    def __str__(self):
        return self.name


class Schema(models.Model):

    """The mothership for filtering the correct tables"""

    name = models.CharField(max_length=100,)

    help_field = models.ManyToManyField(
        SchemaHelpUrl,
        verbose_name='Instruktions felt',
        blank=True,
        )

    is_active = models.BooleanField(
        default=False,
        verbose_name='Aktivt',
        help_text='Om tabellen skal vises',
        )

    is_locked = models.BooleanField(
        default=False,
        verbose_name='Lås',
        help_text='Hvis du låser kan du ikke ændre kolonnerne'
        ' i fremtiden. Du LÅSER kolonnerne.',
        )

    is_obsolete = models.BooleanField(
        default=False,
        verbose_name=' Udgået',
        help_text='Hvis tabellen er udgået, '
        'vil en udgået dato blive sat igennem den her afkrydsning',
        )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Lavet den',
        )

    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Sidst modificeret',
        )

    date_obsolete = models.DateTimeField(
        blank=True, 
        null=True, 
        editable=False,
        verbose_name='Udgået den',
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if instance is_obsolete, if it is, update date_obsolete with
        # timezone.now(). Else if not is_obsolete, replace with None.
        if self.is_obsolete:
            self.date_obsolete = timezone.now()
        elif not self.is_obsolete:
            self.date_obsolete = None

        super().save(*args, **kwargs)


class SchemaColumn(models.Model):

    """Question for schema"""

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,)
    text = models.CharField(max_length=100,)
    is_bool = models.BooleanField(
        default=False,
        verbose_name='Ja/Nej spørgsmål',
        )

    is_editable = models.BooleanField(
        default=False,
        verbose_name='Felt kan ændres',
        )

    class Meta:
        unique_together = ('schema', 'text',)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.schema.is_locked:
            raise SchemaIsLockedError(
                f'{self.schema.name}.is_locked = '
                f'{self.schema.is_locked}, can\'t save'
                )
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.schema.is_locked:
            raise SchemaIsLockedError(
                f'{self.schema.name}.is_locked = '
                f'{self.schema.is_locked}, can\'t delete'
                )
        else:
            super().delete(*args, **kwargs)


class SchemaResponse(models.Model):

    """Response to question set"""

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,)

    qa_set = JSONField()

    instruction = models.ForeignKey(
        SchemaHelpUrl, 
        on_delete=models.PROTECT,
        null=True,)

    user = models.ForeignKey(User, on_delete=models.PROTECT, default=1) # admin
    pub_date = models.DateTimeField(auto_now_add=True,)


    def __str__(self):
        return f'{self.id}'

    def get_questions(self):
        return SchemaColumn.objects.filter(schema=self.schema)

