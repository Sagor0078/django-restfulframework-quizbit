from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer, PracticeHistory
from .serializers import QuestionSerializer, AnswerSerializer, PracticeHistorySerializer

# Retrieve a list of questions
class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# Get details of a specific question
class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# Submit an answer to a question
class SubmitAnswerView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        question = Question.objects.get(id=request.data['question'])
        selected_option = request.data['selected_option']
        is_correct = selected_option == question.correct_option

        # Save the answer
        Answer.objects.create(user=user, question=question, selected_option=selected_option, is_correct=is_correct)

        # Update or create practice history
        history, _ = PracticeHistory.objects.get_or_create(user=user)
        history.total_questions += 1
        if is_correct:
            history.correct_answers += 1
        history.save()

        return Response({"is_correct": is_correct, "message": "Answer submitted successfully!"}, status=status.HTTP_201_CREATED)

# Retrieve a user's practice history
class PracticeHistoryView(generics.RetrieveAPIView):
    serializer_class = PracticeHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return PracticeHistory.objects.get_or_create(user=user)[0]
