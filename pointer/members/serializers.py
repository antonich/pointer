from rest_framework import serializers

from members.models import Member
from users.serializers import UserSerializer
from users.models import User

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = '__all__'

    # def create(self, validated_data):
    #     return Member.objects.create_member(**validated_data)

    def create(self, validated_data):
        user_serial = UserSerializer(data=validated_data['user'])
        if user_serial.is_valid():
            try:
                user = User.objects.get(id=user_serial.data['id'])
                member = Member.objects.create_member(
                    user=user,
                    pointer=validated_data['pointer'],
                )
            except:
                raise serializers.ValidationError("No such user.")
        else:
            raise serializers.ValidationError("Some errors with user.")

        member.save()
        return member
