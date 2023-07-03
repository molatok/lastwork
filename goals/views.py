from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .models.models import GoalCategory, Goal, GoalComment
from .models.board import Board, BoardParticipant
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, generics
from .serializers import GoalCreateSerializer, GoalCategorySerializer, GoalSerializer, GoalCategoryCreateSerializer, \
    GoalCommentCreateSerializer, GoalCommentSerializer, BoardListSerializer, BoardSerializer, \
    BoardParticipantSerializer, BoardCreateSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import filters
from .filters import GoalDateFilter
from .permissions import BoardPermission, CategoryPermission, GoalPermission, GoalCommentPermission
from django.db import transaction


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [CategoryPermission]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )

    filterset_fields = ('board',)
    ordering_fields = ('title', 'created',)
    search_fields = ('title',)

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [CategoryPermission]

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False, board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = (IsAuthenticated,)


class GoalListView(ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (GoalPermission,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ('-priority', 'due_day',)
    ordering = ('-priority',)
    search_fields = ('title',)

    def get_queryset(self):
        return self.model.objects.filter(category__board__participants__user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = (GoalPermission,)

    def get_queryset(self):
        return self.model.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        """
        При удалении цели у нее меняется поле статус на "В архиве"
        """
        instance.status = self.model.Status.archived
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = (IsAuthenticated,)


class GoalCommentListView(ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (GoalCommentPermission,)
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = ('goal',)
    ordering = ('-id',)

    def get_queryset(self):
        return self.model.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = (GoalCommentPermission,)

    def get_queryset(self):
        return self.model.objects.filter(goal__category__board__participants__user=self.request.user)


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermission]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.ARCHIVED
            )
        return instance


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermission]
    pagination_class = LimitOffsetPagination
    serializer_class = BoardListSerializer
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering = ["title"]

    def get_queryset(self):
        return self.model.objects.filter(participants__user=self.request.user, is_deleted=False)
