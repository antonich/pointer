from rest_framework import serializers

from point.models import Pointer, PublicPointer

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

class PublicPointerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicPointer
        fields = '__all__'

    def create(self, validated_data):
        ppoint = Pointer.objects.create_pointer(
            author=validated_data['author'],
            desc=validated_data['description'],
            title=validated_data['title'],
            pdate=validated_data['pointer_date']
        )
        return ppoint
