import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, get_updates_schema, send_message_schema


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        response = requests.get(self.get_url(f'getUpdates?offset={offset}&timeout={timeout}&'
                                             f"allowed_updates=['update_id','message']"))
        json_data = response.json()
        print(json_data)
        result = get_updates_schema().load(json_data)

        return result

    def send_message(self, chat_id: int, text: str):
        url = self.get_url('sendMessage')
        data = {
            "chat_id": chat_id,
            "text": text
        }

        response = requests.post(url, json=data)
        json_data = response.json()

        return json_data
