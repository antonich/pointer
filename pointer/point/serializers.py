from rest_framework import serializers

from django.db import models

from members.models import Member
from point.models import Pointer, PublicPointer, PrivatePointer
from members.serializers import MemberSerializer
from users.serializers import UserSerializer

class PointerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pointer
        exclude = ('date_created',)

    def create(self, validated_data):
        point = Pointer.objects.create_pointer(
            author=validated_data['author'],
            desc=validated_data['description'],
            title=validated_data['title'],
            pdate=validated_data['pointer_date']
        )
        return point

class PointerSerializerData(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Pointer
        exclude = ('date_created',)

class PublicPointerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicPointer
        fields = '__all__'
    #
    # def create(self, validated_data):
    #     ppoint = PublicPointer.objects.create_public_pointer(
    #         author=validated_data['author'],
    #         desc=validated_data['description'],
    #         title=validated_data['title'],
    #         pdate=validated_data['pointer_date']
    #     )
    #     return ppoint

class PrivatePointerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivatePointer
        exclude = ('is_private',)


class FeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pointer
        exclude = ('date_created',)

    def __init__(self, *args, **kwargs):
        try:
            self.user = kwargs['context']['user']
        except:
            pass

        super(FeedItemSerializer, self).__init__(*args, **kwargs)


    def to_representation(self, instance):
         # instance is the model object. create the custom json format by accessing instance attributes normaly and return it
        data = dict()
        pointer_serializer = PointerSerializerData(instance)

        member_list = Member.objects.going_members_without_active_user(instance, self.user)
        try:
            pointed = Member.objects.get(pointer=instance, user=self.user)
            pointed_serial = MemberSerializer(pointed)
        except:
            pointed_serial = None

        member_serializer= MemberSerializer(member_list, many=True)


        for attr, value in instance.__dict__.iteritems():
            if not attr.startswith('_'):
                data[attr] = value

        representation = {
            'pointer': pointer_serializer.data,
            'pointed': pointed_serial.data if pointed_serial != None else '',
            'members': member_serializer.data
         }

        return representation

class PointerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pointer
        exclude = ('date_created',)

    def to_representation(self, instance):
         # instance is the model object. create the custom json format by accessing instance attributes normaly and return it
        data = dict()

        pointer_serializer = PointerSerializerData(instance)
        member_list = Member.objects.going_members(instance)
        member_serializer= MemberSerializer(member_list, many=True)

        # getting only needed attributes
        for attr, value in instance.__dict__.iteritems():
            if not attr.startswith('_'):
                data[attr] = value

        representation = {
            'pointer': pointer_serializer.data,
            'members': member_serializer.data
         }

        return representation
