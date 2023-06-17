from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Answer, Question, Survey, Variant
from .permissions import IsAdminOrReadOnly
from .serializers import (
    AnswerSerializer,
    QuestionSerializer,
    ResultViewSerializer,
    SurveySerializerAdmin,
    SurveySerializerPublic,
    VariantSerializer,
)
from .validators import validate_user_id


@extend_schema(tags=["Опросы"])
@extend_schema_view(
    list=extend_schema(
        summary='Список опросов (c вопросами и вариантами ответов)'
    ),
    retrieve=extend_schema(
        summary='Деталка опроса (c вопросами и вариантами ответов)'
    ),
    create=extend_schema(summary='Создать опрос'),
    update=extend_schema(summary='Изменить опрос'),
    partial_update=extend_schema(summary='Изменить опрос частично'),
    destroy=extend_schema(summary='Удалить опрос'),
)
class SurveyViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_active',)
    http_method_names = ('get', 'post', 'put', 'delete')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Survey.objects.all()
        return Survey.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return SurveySerializerAdmin
        return SurveySerializerPublic


@extend_schema(tags=["Вопросы"])
@extend_schema_view(
    list=extend_schema(summary='Список вопросов'),
    retrieve=extend_schema(summary='Деталка вопроса (с вариантами ответов)'),
    create=extend_schema(summary='Создать вопрос'),
    update=extend_schema(summary='Изменить вопрос'),
    partial_update=extend_schema(summary='Изменить вопрос частично'),
    destroy=extend_schema(summary='Удалить вопрос'),
)
class QuestionViewSet(CreateModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ('get', 'post', 'put', 'delete')

    def get_object(self):
        survey_id = self.kwargs.get('survey_id')
        question_id = self.kwargs.get('pk')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise Http404("Опрос id {} не существует".format(survey_id))
        try:
            questions = survey.questions.get(id=question_id)
            return questions
        except Question.DoesNotExist:
            raise Http404("Вопрос id {} не существует".format(question_id))

    def perform_create(self, serializer):
        survey_id = self.kwargs.get('survey_id')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise Http404("Опрос id {} не существует".format(survey_id))
        serializer.save(survey=survey)


@extend_schema_view(
    list=extend_schema(summary='Получить список вариантов ответа на вопрос',
                       tags=["Прохождение опроса и просмотр результатов"]),
    retrieve=extend_schema(summary='Получить один вариант ответа на вопрос',
                           tags=["Прохождение опроса и просмотр результатов"]),
    create=extend_schema(summary='Создать вариант ответа',
                         tags=["Варианты ответов"]),
    update=extend_schema(summary='Изменить вариант ответа',
                         tags=["Варианты ответов"]),
    partial_update=extend_schema(summary='Изменить вариант ответа частично',
                                 tags=["Варианты ответов"]),
    destroy=extend_schema(summary='Удалить вариант ответа',
                          tags=["Варианты ответов"]),
)
class VariantViewSet(CreateModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     ListModelMixin,
                     GenericViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'put', 'delete')

    def perform_create(self, serializer):
        survey_id = self.kwargs.get('survey_id')
        question_id = self.kwargs.get('question_id')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise Http404("Опрос id {} не существует".format(survey_id))
        try:
            question = Question.objects.get(id=question_id, survey=survey)
        except Question.DoesNotExist:
            raise Http404("Вопрос id {} не существует в опросе id {}".format(
                question_id, survey_id
            ))
        serializer.save(question=question)

    def get_queryset(self):
        survey_id = self.kwargs.get('survey_id')
        question_id = self.kwargs.get('question_id')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise Http404("Опрос id {} не существует".format(survey_id))
        try:
            question = Question.objects.get(id=question_id, survey=survey)
        except Question.DoesNotExist:
            raise Http404("Вопрос id {} не существует в опросе id {}".format(
                question_id, survey_id
            ))
        variants = question.variants.all()
        if not variants.exists():
            raise Http404("Вопрос id {} не имеет вариантов ответа".format(
                question_id
            ))
        return variants


@extend_schema(tags=["Прохождение опроса и просмотр результатов"])
@extend_schema_view(
    create=extend_schema(summary='Ответить на вопрос'),
    update=extend_schema(summary='Изменить ответ на вопрос'),
    partial_update=extend_schema(summary='Изменить ответ на вопрос частично'),
    destroy=extend_schema(summary='Удалить ответ на вопрос'),
)
class AnswerViewSet(CreateModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    GenericViewSet):
    queryset = Answer
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ('get', 'post', 'put', 'delete')

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        validate_user_id(user_id)
        survey_id = self.kwargs.get('survey_id')
        question_id = self.kwargs.get('question_id')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise Http404("Опрос id {} не существует".format(survey_id))
        try:
            question = Question.objects.get(id=question_id, survey=survey)
        except Question.DoesNotExist:
            raise Http404("Вопрос id {} не существует в опросе id {}".format(
                question_id, survey_id
            ))
        serializer.save(question=question, survey=survey, user_id=user_id)

    def perform_update(self, serializer):
        user_id = self.kwargs.get('user_id')
        if user_id:
            validate_user_id(user_id)
        serializer.save()

    def get_queryset(self):
        survey_id = self.kwargs.get('survey_id')
        question_id = self.kwargs.get('question_id')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise Http404("Опрос id {} не существует".format(survey_id))
        try:
            question = Question.objects.get(id=question_id, survey=survey)
        except Question.DoesNotExist:
            raise Http404("Вопрос id {} не существует в опросе id {}".format(
                question_id, survey_id
            ))
        answers = question.answers.all()
        if not answers.exists():
            raise Http404("Вопрос id {} не имеет ответов пользователя".format(
                question_id
            ))
        return answers


@extend_schema(tags=["Прохождение опроса и просмотр результатов"])
@extend_schema_view(
        list=extend_schema(
            summary='Просмотр результатов всех опросов по ID пользователя'
        ),
    )
class ResultViewSet(ListModelMixin,
                    GenericViewSet):
    serializer_class = ResultViewSerializer
    queryset = Survey.objects.all()
    permission_classes = [AllowAny, ]
