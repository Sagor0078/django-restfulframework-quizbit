# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, PracticeHistoryViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'practice-history', PracticeHistoryViewSet, basename='practice-history')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
]