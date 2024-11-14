# serializers.py
from rest_framework import serializers
from .models import Category, Question, Choice, UserAnswer
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from django.contrib.auth.models import User

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid question example',
            value={
                'id': 1,
                'title': 'What is Python?',
                'difficulty': 'medium',
                'points': 10,
                'category_name': 'Programming'
            },
            request_only=False,
            response_only=True,
        )
    ]
)

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'content']

class QuestionListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'difficulty', 'points', 'category_name']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid question detail example',
            value={
                'id': 1,
                'title': 'What is Python?',
                'content': 'Choose the best description of Python.',
                'difficulty': 'medium',
                'points': 10,
                'category_name': 'Programming',
                'choices': [
                    {'id': 1, 'content': 'A programming language'},
                    {'id': 2, 'content': 'A type of snake'}
                ]
            },
            request_only=False,
            response_only=True,
        )
    ]
)
class QuestionDetailSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name')
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'difficulty', 'points', 'category_name', 'choices']

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['question', 'selected_choice']

    def create(self, validated_data):
        user = self.context['request'].user
        question = validated_data['question']
        selected_choice = validated_data['selected_choice']
        
        # Check if the selected choice is correct
        is_correct = selected_choice.is_correct
        
        # Create or update the user answer
        user_answer, created = UserAnswer.objects.update_or_create(
            user=user,
            question=question,
            defaults={
                'selected_choice': selected_choice,
                'is_correct': is_correct
            }
        )
        
        return user_answer

class PracticeHistorySerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='question.title')
    selected_answer = serializers.CharField(source='selected_choice.content')
    
    class Meta:
        model = UserAnswer
        fields = ['question_title', 'selected_answer', 'is_correct', 'answered_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user