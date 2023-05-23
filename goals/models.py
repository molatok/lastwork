from django.db import models
from django.utils import timezone
from core.models import CustomUser
from django.utils import timezone


class GoalCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

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

    STATUS_CHOICES = [
        (1, "К выполнению"),
        (2, "В процессе"),
        (3, "Выполнено"),
        (4, "Архив"),
    ]

    PRIORITY_CHOICES = [
        (1, "Низкий"),
        (2, "Средний"),
        (3, "Высокий"),
        (4, "Критический"),
    ]

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(CustomUser, verbose_name="Автор", on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.CASCADE)
    due_date = models.DateTimeField(verbose_name="Дата выполнения", null=True)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=1)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=PRIORITY_CHOICES, default=1)

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
