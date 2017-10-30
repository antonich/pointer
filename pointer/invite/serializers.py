from rest_framework import serializers

from invite.models import Invite

class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = '__all__'

    def create(self, validated_data):
        invite = Invite.objects.create_invite(
            user=validated_data['to_user'],
            pointer=validated_data['pointer'],
        )
        return invite
