# quiz_app/views.py

from rest_framework import generics, permissions, serializers
from django.contrib.auth import get_user_model, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import QuizField, QuizResult, QuizAnswer, Question, Option
from .serializers import CustomUserSerializer, QuizSerializer, QuizFieldSerializer, QuizResultSerializer
from django.db.models import Avg


class UserLogin(TokenObtainPairView):
    serializer_class = TokenObtainPairView.serializer_class


class UserRegistration(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


class UserLogout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'User logged out successfully.'}, status=200)


class QuizList(generics.ListAPIView):
    queryset = QuizField.objects.all()
    serializer_class = QuizFieldSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuizDetail(generics.RetrieveAPIView):
    queryset = QuizField.objects.all()
    serializer_class = QuizFieldSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuizQuestions(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, field_id, *args, **kwargs):
        quiz_field = generics.get_object_or_404(QuizField, pk=field_id)
        questions = quiz_field.questions.all()
        serializer = QuizSerializer(questions, many=True)
        return Response(serializer.data, status=200)


class SubmitQuiz(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = request.data.get('answers', [])

        quiz_result = QuizResult.objects.create(user=user)
        correct_answers = 0

        for answer in data:
            question_id = answer['question']
            option_id = answer['option']

            try:
                question = Question.objects.get(pk=question_id)
                selected_option = Option.objects.get(pk=option_id)
            except Question.DoesNotExist or Option.DoesNotExist:
                return Response({'message': 'Invalid question or option'}, status=400)

            if selected_option.is_correct:
                correct_answers += 1

            quiz_answer = QuizAnswer.objects.create(quiz_result=quiz_result, question=question,
                                                    selected_option=selected_option)

        total_questions = len(data)
        percentage_score = (correct_answers / total_questions) * 100

        return Response({
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'percentage_score': percentage_score
        }, status=200)


class UserStatistics(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        quizzes_taken = user.quiz_results.count()

        if quizzes_taken > 0:
            total_score = sum(result.score for result in user.quiz_results.all())
            average_score = total_score / quizzes_taken
        else:
            total_score = 0
            average_score = 0

        return Response({
            'quizzes_taken': quizzes_taken,
            'total_score': total_score,
            'average_score': average_score
        }, status=200)


class UserRanking(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = get_user_model().objects.annotate(avg_score=Avg('quiz_results__score')).order_by('-avg_score')
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=200)
