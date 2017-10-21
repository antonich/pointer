from rest_framework import serializers

from members.models import Member

class MemberSerializer(serializers.ModelSerializer):
    """
        Pointer serializer
    """

    class Meta:
        model = Member
        fields = '__all__'
        exclude = ('pointer',)
