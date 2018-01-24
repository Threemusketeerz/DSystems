from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from jsonfield import JSONField

from .exceptions import SchemaIsLockedError


class SchemaUrl(models.Model):

    """This will be initialized above all the fields. Beneath the header. this
    will contain urls referencing links connected to the schema."""

    url = models.CharField(max_length=200)
    name = models.CharField(max_length=50,)
    help_text = models.TextField(default='',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Instruktion'
        verbose_name_plural = 'Instruktioner'


class Schema(models.Model):

    """The mothership for filtering the correct tables"""

    name = models.CharField(max_length=100,)

    help_field = models.ManyToManyField(
        SchemaUrl,
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
        help_text="""Hvis du låser kan du ikke ændre kolonnerne 
        i fremtiden. Du LÅSER kolonnerne. HVIS DU PRØVER VIL DU FÅ ERROR CODE
        500""",
        )

    is_obsolete = models.BooleanField(
        default=False,
        verbose_name=' Udgået',
        help_text='Hvis tabellen er udgået, '
        'vil en udgået dato blive sat igennem den her afkrydsning',
        )

    has_ancestor = models.BooleanField(
        default=False,
        verbose_name='Har forfædre',
        help_text="""Hvis tabellen har en ældre version af sig, for at fortælle
        systemet at den skal lave et link der referere tilbage til det skema,
        skal denne være afkrydset""",
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

    class Meta:
        verbose_name = 'Skema'
        verbose_name_plural = 'Skemaer'

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

    is_editable_once = models.BooleanField(
        default=False,
        verbose_name='Felt kan ændres, en enkelt gang',
        )

    class Meta:
        unique_together = ('schema', 'text',)
        verbose_name = 'Kolonner'

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.schema.is_locked:
            # CAUSING 500 INTERNAL ERROR
            raise SchemaIsLockedError(
                f'{self.schema.name}.is_locked = '
                f'{self.schema.is_locked}, can\'t save'
                )
        else:
            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        if self.schema.is_locked:
            # CAUSING 500 INTERNAL ERROR
            raise SchemaIsLockedError(
                f'{self.schema.name}.is_locked = '
                f'{self.schema.is_locked}, can\'t delete'
                )
            return
        else:
            super().delete(*args, **kwargs)


class SchemaResponse(models.Model):

    """Response to question set"""

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,)

    qa_set = JSONField()

    instruction = models.ForeignKey(
        SchemaUrl, 
        on_delete=models.PROTECT,
        null=True,)

    user = models.ForeignKey(User, on_delete=models.PROTECT, default=1) # admin
    pub_date = models.DateTimeField(auto_now_add=True,)


    def __str__(self):
        return f'{self.id}'

    def get_questions(self):
        return SchemaColumn.objects.filter(schema=self.schema)


class SchemaHistoryManager(models.Manager):
    def obsolete(self):
        return Schema.objects.filter(is_obsolete=True)

    def new(self):
        return Schema.objects.filter(is_obsolete=False)


class SchemaHistoryLog(models.Model):
    history = SchemaHistoryManager()

    # I have turned these two around, for some reason the logic is opposite.
    # Don't know why yet.
    obsolete_schema = models.ForeignKey(
        Schema, related_name='new', on_delete=models.DO_NOTHING,
        blank=True, null=True, limit_choices_to={'is_obsolete': True},
        verbose_name='Udgåede skemaer',
        )
    new_schema = models.ForeignKey(
        Schema, related_name='obsolete', on_delete=models.DO_NOTHING,
        blank=True, null=True, limit_choices_to={'is_obsolete': False},
        verbose_name='Ikke udgåede skemaer',
        )
    pub_date = models.DateTimeField(auto_now_add=True)

    """ Manager that handles set of objects for OLD_SCHEMA = model.is_obsolete.
        And NEW_SCHEMA != model.is_obsolete
    """

    class Meta:
        verbose_name = 'Skema Historik'
        verbose_name_plural = 'Skema Historik'

    def __str__(self):
        return f'{self.obsolete_schema.name} -> {self.new_schema.name}'
