from django.urls import include, path
from rest_framework import routers

from .spectacular.urls import urlpatterns as doc_urls
from .views import (
    AnswerViewSet,
    QuestionViewSet,
    ResultViewSet,
    SurveyViewSet,
    VariantViewSet,
)

# app_name = 'api'

router = routers.DefaultRouter()
router.register(
    prefix='surveys',
    viewset=SurveyViewSet,
    basename='surveys',
)
router.register(
    prefix=r'surveys/(?P<survey_id>[\d]+)/questions',
    viewset=QuestionViewSet,
    basename='questions',
)
router.register(
    prefix=r'surveys/(?P<survey_id>[\d]+)/questions/(?P<question_id>[\d]+)'
           r'/variants',
    viewset=VariantViewSet,
    basename='variants',
)
router.register(
    prefix=r'(?P<user_id>[\d]+)/surveys/(?P<survey_id>[\d]+)/questions'
           r'/(?P<question_id>[\d]+)/answers',
    viewset=AnswerViewSet,
    basename='answers',
)
router.register(
    prefix=r'(?P<user_id>[\d]+)/surveys',
    viewset=ResultViewSet,
    basename='answer_lists',
)
urlpatterns = [
    path('v1/', include(router.urls)),
]
urlpatterns += doc_urls
