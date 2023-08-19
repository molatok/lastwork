from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from bot.serializers import TgUserVerCodSerializer
from bot.tg import tg_client


class TgUserUpdate(generics.UpdateAPIView):
    """
        Представление для обновления информации о пользователе Telegram.
        Позволяет обновлять данные о пользователе на основе верификационного кода.
        Для использования требуется аутентификация пользователя.

        Методы:
        - get_object: Получает объект TgUser на основе верификационного кода.
        - perform_update: Выполняет обновление данных с сохранением аутентифицированного пользователя.
        - get_serializer_context: Добавляет в контекст сериализатора экземпляр tg_client для отправки сообщений Telegram.
        """
    model = TgUser
    serializer_class = TgUserVerCodSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('patch',)

    def get_object(self):
        try:
            obj = self.model.objects.get(verification_code=self.request.data.get('verification_code'))
        except self.model.DoesNotExist:
            raise ValidationError({'verification_code': 'Неправильный верификационный код'})

        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tg_client'] = tg_client
        return context
