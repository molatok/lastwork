from django.db import models
from django.utils import timezone
from core.models import CustomUser
from django.utils import timezone
from .board import Board


class GoalCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(CustomUser, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Goal(models.Model):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    class Status(models.IntegerChoices):
        PENDING = 1, 'Pending'
        IN_PROGRESS = 2, 'In Progress'
        COMPLETED = 3, 'Completed'
        ARCHIVED = 4, 'Archived'

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(CustomUser, verbose_name="Автор", on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.CASCADE)
    due_date = models.DateTimeField(verbose_name="Дата выполнения", null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Status.choices, default=Status.PENDING)

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)


class GoalComment(models.Model):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст")
    user = models.ForeignKey(CustomUser, verbose_name="Автор", on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")
    is_deleted = models.BooleanField(verbose_name="Удален", default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


