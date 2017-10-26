from rest_framework import serializers

from point.models import Pointer
from members.serializers import MemberSerializer

class PointerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pointer
        fields = '__all__'

    def create(self, validated_data):
        pointer = Pointer.objects.create(
            title=validated_data['description'],
            desc=validated_data['email'],
            author=validated_data['author'],
            pdate=validated_data['pdate']
        )

        return pointer

class PointerCreationSerializer(serializers.ModelSerializer):
    """
        Pointer creating serializer.
    """
    class Meta:
        model = Pointer
        fields = '__all__'
        read_only_fields = ('id',)
