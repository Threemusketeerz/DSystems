from rest_framework import serializers

from .models import SchemaResponse


class SchemaResponseSerializer(serializers.ModelSerializer):

    """Serializes data for DataTables use. This might very well be unnecessary"""

    class Meta:
        model = SchemaResponse
        fields = ('__all__')
