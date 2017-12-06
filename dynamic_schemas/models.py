from django.db import models
from jsonfield import JSONField
# Create your models here.


class SchemaHelpUrl(models.Model):

    """This will be initialized above all the fields. Beneath the header. this
    will contain urls referencing links connected to the schema."""

    url = models.URLField()
    link_name = models.CharField(max_length=50)
    help_text = models.TextField(default='')

    def __str__(self):
        return self.link_name


class Schema(models.Model):

    """The mothership for filtering the correct tables"""

    name = models.CharField(max_length=100)

    help_field = models.ManyToManyField(SchemaHelpUrl,
                                        verbose_name='Instruktions felt',
                                        )

    def __str__(self):
        return self.name


class SchemaQuestion(models.Model):

    """Question for schema"""

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_response_bool = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text


class SchemaResponse(models.Model):

    """Response to question set"""

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    qa_set = JSONField()

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    def get_questions(self):
        return SchemaQuestion.objects.filter(schema=self.schema)


