from rest_framework import serializers

from point.models import Pointer

class PointerSerializer(serializers.ModelSerializer):
    """
        Pointer serializers
    """

    class Meta:
        model = Pointer
        fields = '__all__'
