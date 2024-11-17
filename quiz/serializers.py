from rest_framework import serializers
from .models import Question, Answer, PracticeHistory

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'options', 'correct_option']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'user', 'selected_option', 'is_correct', 'submitted_at']

class PracticeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeHistory
        fields = ['user', 'total_questions', 'correct_answers', 'last_practiced']