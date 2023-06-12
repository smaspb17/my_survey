from datetime import date
# from django.utils import timezone
from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    StringRelatedField,
    ValidationError,
)

from .models import Question, Survey, Variant


class SurveySerializerAdmin(ModelSerializer):
    questions = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'is_active',
                  'start_date', 'end_date', 'questions',)
        read_only_fields = ('start_date',)

    def create(self, validated_data):
        start_date = date.today()
        # start_date = timezone.localdate()
        end_date = validated_data.get('end_date')
        delta = end_date - start_date
        if delta.days < 3:
            raise ValidationError(
                "Дата окончания - не менее 3 дней от сегодняшнего дня"
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        start_date = instance.start_date
        end_date = validated_data.get('end_date')
        delta = end_date - start_date
        if delta.days < 3:
            raise ValidationError(
                "Дата окончания - не менее 3 дней от сегодняшнего дня"
            )
        if end_date < date.today():
            raise ValidationError(
                "Дата окончания не может быть прошедшим днем"
            )
        return super().update(instance, validated_data)


class SurveySerializerPublic(ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'start_date', 'end_date',)


class QuestionSerializer(ModelSerializer):
    survey = SlugRelatedField(queryset=Question.objects,
                              slug_field='name')
    variants = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'survey', 'variants')


class VariantSerializer(ModelSerializer):
    class Meta:
        model = Variant
        fields = ('id', 'text', 'questions')
