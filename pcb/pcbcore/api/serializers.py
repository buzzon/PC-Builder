from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from pcbcore.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Brand
        fields = '__all__'


class SocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socket
        fields = '__all__'


class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = '__all__'


class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = '__all__'


class MemoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryType
        fields = '__all__'


class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = '__all__'


class FormfactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formfactor
        fields = '__all__'


class ChipsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chipset
        fields = '__all__'


class MotherBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherBoard
        fields = '__all__'


class SSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSD
        fields = '__all__'


class HDDSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDD
        fields = '__all__'


class PowerSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerSupply
        fields = '__all__'


