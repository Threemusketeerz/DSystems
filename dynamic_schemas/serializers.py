from rest_framework import serializers

from .models import SchemaResponse


class SchemaResponseSerializer(serializers.ModelSerializer):

    """Serializes data for DataTables use."""

    class Meta:
        model = SchemaResponse
        fields = ('__all__')

        
