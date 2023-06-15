from datetime import date
# from django.utils import timezone
from rest_framework.serializers import (
    DateField,
    ModelSerializer,
    SlugRelatedField,
    StringRelatedField,
    ValidationError,
)

from .models import Question, Survey, Variant


class QuestionViewSerializer(ModelSerializer):
    variants = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'variants',)


class SurveySerializerAdmin(ModelSerializer):
    questions = QuestionViewSerializer(many=True)
    # questions = StringRelatedField(many=True, read_only=True)
    start_date = DateField(default=date.today())

    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'is_active',
                  'start_date', 'end_date', 'questions',)
        # read_only_fields = ('start_date',)

    def create(self, validated_data):
        # start_date = date.today()
        # start_date = timezone.localdate()
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        delta = end_date - start_date
        if start_date < date.today() or end_date < date.today():
            raise ValidationError(
                "Прошедший день ставить нельзя"
            )
        elif end_date < start_date:
            raise ValidationError(
                "Начало опроса не может быть позже окончания"
            )
        elif start_date != date.today():
            raise ValidationError(
                "Дата старта должна быть сегодняшним днем"
            )
        elif delta.days < 3:
            raise ValidationError(
                "Продолжительность опроса - не менее 3 дней"
            )
        # выполняется в конце валидации
        # validated_data['start_date'] = date.today()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        start_date = instance.start_date
        end_date = validated_data.get('end_date')
        delta = end_date - start_date
        if start_date < date.today() or end_date < date.today():
            raise ValidationError(
                "Прошедший день ставить нельзя"
            )
        elif end_date < start_date:
            raise ValidationError(
                "Начало опроса не может быть позже окончания"
            )
        elif delta.days < 3:
            raise ValidationError(
                "Продолжительность опроса - не менее 3 дней"
            )
        return super().update(instance, validated_data)


class SurveySerializerPublic(ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'start_date', 'end_date',)


class VariantViewSerializer(ModelSerializer):

    class Meta:
        model = Variant
        fields = ('id', 'text',)


class QuestionSerializer(ModelSerializer):
    # survey = StringRelatedField(read_only=True)
    survey = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    variants = VariantViewSerializer(many=True)
    # variants = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'survey', 'variants')


class VariantSerializer(ModelSerializer):
    question = StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Variant
        fields = ('id', 'text', 'question')
        read_only_fields = ('question',)
