import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, get_updates_schema, send_message_schema


import requests

class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        # Оставляем эту функцию без изменений

    def get_updates(self, offset: int = 0, timeout: int = 60):
        # Оставляем эту функцию без изменений

    def send_message(self, chat_id: int, text: str):
        """
               Отправление сообщения пользователю от бота.
               Args:
                   chat_id: int
                   text: str
               Returns:
                   SendMessageResponse
               """
        url = self.get_url('sendMessage')
        data = {
            "chat_id": chat_id,
            "text": text
        }

        response = requests.post(url, json=data)
        json_data = response.json()
        result = send_message_schema().load(json_data)

        return result




# cl = TgClient("6187763368:AAGEiOYId1RLD3jQd-vgBeWMv5eHps33j2c")
# print(cl.get_updates(offset=0, timeout=60))
#

# cl = TgClient("6187763368:AAGEiOYId1RLD3jQd-vgBeWMv5eHps33j2c")
# print(cl.send_message(726484566, "hello"))
