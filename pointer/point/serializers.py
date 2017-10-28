from rest_framework import serializers

from point.models import Pointer
from members.serializers import MemberSerializer

class PointerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pointer
        fields = '__all__'

    def create(self, validated_data):
        point = Pointer.objects.create_pointer(
            author=validated_data['author'],
            desc=validated_data['description'],
            title=validated_data['title'],
            pdate=validated_data['pointer_date']
        )
        return point
