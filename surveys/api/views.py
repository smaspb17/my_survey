# from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Question, Survey, Variant
from .permissios import IsAdminOrReadOnly
from .serializers import (
    QuestionSerializer,
    SurveySerializerAdmin,
    SurveySerializerPublic,
    VariantSerializer,
)


@extend_schema(tags=["Опросы"])
@extend_schema_view(
    list=extend_schema(summary='Список опросов'),
    retrieve=extend_schema(summary='Деталка опроса'),
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
    retrieve=extend_schema(summary='Деталка вопроса'),
    create=extend_schema(summary='Создать вопрос'),
    update=extend_schema(summary='Изменить вопрос'),
    partial_update=extend_schema(summary='Изменить вопрос частично'),
    destroy=extend_schema(summary='Удалить вопрос'),
)
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ('get', 'post', 'put', 'delete')

    def get_queryset(self):
        survey = get_object_or_404(
            klass=Survey, id=self.kwargs.get('survey_id'))
        print(survey)
        return survey.questions.all()

    def perform_create(self, serializer):
        # survey = get_object_or_404(
        #     klass=Survey, id=self.kwargs.get('survey_id'))
        serializer.save(
            survey=Survey.objects.get(id=self.kwargs.get('survey_id')))

    # def get_queryset(self):
    #     review = get_object_or_404(
    #         klass=Review, id=self.kwargs.get('review_id')
    #     )
    #     return review.comments.all()

    # def perform_create(self, serializer):
    #     review = get_object_or_404(
    #         klass=Review, id=self.kwargs.get('review_id')
    #     )
    #     serializer.save(author=self.request.user, review=review)


class VariantViewSet(CreateModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     GenericAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer

    def create(self, request, *args, **kwargs):
        print(self, request, *args, **kwargs, set="\n")
        return super().create(request, *args, **kwargs)
