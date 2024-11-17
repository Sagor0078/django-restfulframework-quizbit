from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Question, Answer, PracticeHistory

class QuizAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.question = Question.objects.create(
            title='Sample Question',
            content='Sample Content',
            options={"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
            correct_option='A'
        )

    def test_submit_answer_correct(self):
        response = self.client.post('/api/answers/', {
            'question': self.question.id,
            'selected_option': 'A'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['is_correct'])

    def test_submit_answer_incorrect(self):
        response = self.client.post('/api/answers/', {
            'question': self.question.id,
            'selected_option': 'B'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['is_correct'])

    def test_submit_answer_missing_fields(self):
        response = self.client.post('/api/answers/', {
            'question': self.question.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_practice_history(self):
        # Submit a correct answer
        self.client.post('/api/answers/', {
            'question': self.question.id,
            'selected_option': 'A'
        }, format='json')

        # Retrieve practice history
        response = self.client.get('/api/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_questions'], 1)
        self.assertEqual(response.data['correct_answers'], 1)