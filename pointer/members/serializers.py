from rest_framework import serializers

from members.models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def create(self, validated_data):
        return Member.objects.create_member(**validated_data)
