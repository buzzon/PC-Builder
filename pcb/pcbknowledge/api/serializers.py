from rest_framework import serializers

from pcbknowledge.models import *


class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = ['id', 'coefficient', 'component']


class EssenceSerializer(serializers.ModelSerializer):
    factors = FactorSerializer(required=False, many=True)

    class Meta:
        model = Essence
        fields = ['id', 'title', 'next_question', 'factors']


class QuestionSerializer(serializers.ModelSerializer):
    essences = EssenceSerializer(required=False, many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'next', 'component_variable', 'essences']

    def create(self, validated_data):
        essences_data = validated_data.pop('essences')
        question = Question.objects.create(**validated_data)
        for essence in essences_data:
            factors_data = essence.pop('factors')
            essence = Essence.objects.create(question=question, **essence)
            for factor in factors_data:
                Factor.objects.create(essence=essence, **factor)
        return question
