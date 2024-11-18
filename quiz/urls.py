from django.urls import path
from .views import QuestionListView, QuestionDetailView, SubmitAnswerView, PracticeHistoryView
from django.conf.urls import handler400, handler403, handler404, handler500


urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('answers/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('history/', PracticeHistoryView.as_view(), name='practice-history'),
]


handler400 = 'quiz.views.bad_request'
handler403 = 'quiz.views.permission_denied'
handler404 = 'quiz.views.page_not_found'
handler500 = 'quiz.views.server_error'