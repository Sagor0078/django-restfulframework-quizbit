from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Question, UserAnswer
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
from .serializers import (
    QuestionListSerializer,
    QuestionDetailSerializer,
    UserAnswerSerializer,
    PracticeHistorySerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List all questions",
        description="Returns a list of all available quiz questions.",
        tags=["questions"],
    ),
    retrieve=extend_schema(
        summary="Get question details",
        description="Returns detailed information about a specific question.",
        tags=["questions"],
    ),
)
class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return QuestionListSerializer
        return QuestionDetailSerializer

    @extend_schema(
        summary="Submit answer to question",
        description="Submit a user's answer to a specific question.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "choice_id": {
                        "type": "integer",
                        "description": "ID of the selected choice",
                    }
                },
            }
        },
        responses={200: UserAnswerSerializer},
        tags=["questions"],
    )
    @action(detail=True, methods=["post"])
    def submit_answer(self, request, pk=None):
        question = self.get_object()
        serializer = UserAnswerSerializer(
            data={
                "question": question.id,
                "selected_choice": request.data.get("choice_id"),
            },
            context={"request": request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        summary="Get user practice history",
        description="Returns a list of all practice attempts by the current user.",
        tags=["practice"],
    ),
)
class PracticeHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PracticeHistorySerializer

    def get_queryset(self):
        return UserAnswer.objects.filter(user=self.request.user).order_by(
            "-answered_at"
        )


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
