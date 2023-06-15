from django.urls import include, path
from rest_framework import routers

from .spectacular.urls import urlpatterns as doc_urls
from .views import QuestionViewSet, SurveyViewSet, VariantViewSet

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
    prefix=r'surveys/(?P<survey_id>[\d]+)/questions/(?P<question_id>[\d]+)/variants',
    viewset=VariantViewSet,
    basename='variants',
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
urlpatterns += doc_urls
