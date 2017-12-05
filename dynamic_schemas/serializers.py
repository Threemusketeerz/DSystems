from rest_framework import serializers

from .models import SchemaResponse


class SchemaResponseSerializer(serializers.ModelSerializer):

    """Serializes data for DataTables use."""

    class Meta:
        model = SchemaResponse
        fields = ('__all__')


# Custom serializer here with __inti__
# class SchemaColumnSerializer(serializers.Serializer):

    # """Serializes column data, consisting of questions"""

    # def __init__(self, schema, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # schema_questions = schema.schemaquestion_set.all()
        # for question in schema_questions:
            # self.fields[question.text] =Vk


