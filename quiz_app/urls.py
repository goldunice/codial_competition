# quiz_app/urls.py

from django.urls import path
from .views import (
    UserLogin, UserRegistration, UserLogout, QuizList, QuizDetail, QuizQuestions,
    SubmitQuiz, UserStatistics, UserRanking
)

urlpatterns = [
    path('auth/login/', UserLogin.as_view(), name='user-login'),
    path('auth/register/', UserRegistration.as_view(), name='user-registration'),
    path('auth/logout/', UserLogout.as_view(), name='user-logout'),
    path('quiz/fields/', QuizList.as_view(), name='quiz-field-list'),
    path('quiz/fields/<int:pk>/', QuizDetail.as_view(), name='quiz-field-detail'),
    path('quiz/questions/<int:field_id>/', QuizQuestions.as_view(), name='quiz-questions'),
    path('quiz/submit/', SubmitQuiz.as_view(), name='submit-quiz'),
    path('user/statistics/', UserStatistics.as_view(), name='user-statistics'),
    path('ranking/', UserRanking.as_view(), name='user-ranking'),
]
