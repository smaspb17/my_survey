from datetime import date
# from django.utils import timezone
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    CharField,
    DateField,
    ModelSerializer,
    SlugRelatedField,
    ValidationError,
)

from .validators import validate_user_id

from .models import Answer, Question, Survey, Variant


class VariantSerializer(ModelSerializer):
    """Варианты ответов"""
    class Meta:
        model = Variant
        fields = ('id', 'text',)

    def create(self, validated_data):
        question_type = validated_data.get('question').type
        if question_type == Question.Type.TEXT:
            raise ValidationError(
                "Данный вопрос текстовый, без вариантов ответа"
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        question_type = instance.question.type
        if question_type == Question.Type.TEXT:
            raise ValidationError(
                "Данный вопрос текстовый, без вариантов ответа"
            )
        return super().update(instance, validated_data)


class QuestionSerializer(ModelSerializer):
    """Вопросы"""
    variants = VariantSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'variants',)


class SurveySerializerAdmin(ModelSerializer):
    """Опросы (для админа)"""
    questions = QuestionSerializer(many=True, read_only=True)
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
        # выполняется в конце валидации если нужно
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


class FromContext(object):
    """Обход ограчения UniqueTogetherValidator в части обязательных полей"""
    requires_context = True

    def __init__(self, value_fn):
        self.value_fn = value_fn

    def __call__(self, serializer_field):
        self.value = self.value_fn(serializer_field.context)
        return self.value


class AnswerSerializer(ModelSerializer):
    """Ответы на вопросы"""
    user_id = CharField(
        max_length=10,
        read_only=True,
        default=FromContext(
            lambda context: context.get('view').kwargs['user_id']
        )
    )
    question = SlugRelatedField(
        slug_field='text',
        read_only=True,
        default=FromContext(
            lambda context: context.get('view').kwargs['question_id']
        )
    )
    survey = SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=FromContext(
            lambda context: context.get('view').kwargs['survey_id']
        )
    )

    class Meta:
        model = Answer
        fields = ('user_id', 'survey', 'question', 'answer',)
        validators = [
            UniqueTogetherValidator(
                queryset=Answer.objects.all(),
                fields=['question', 'survey', 'user_id'],
                message='Вы уже отвечали на данный вопрос',
            )
        ]

    def validate_user_id(self, value):
        validate_user_id(value)
        return value


class SurveySerializerPublic(ModelSerializer):
    """Активные опросы (для пользователя)"""
    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'start_date', 'end_date',)


class AnswerListSerializer(ModelSerializer):
    question = SlugRelatedField(
        slug_field='text',
        read_only=True,
    )

    class Meta:
        model = Answer
        fields = ('question', 'answer',)


class ResultViewSerializer(ModelSerializer):
    """Результаты опросов"""
    answers = AnswerListSerializer(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'name', 'description',
                  'start_date', 'end_date', 'answers')
