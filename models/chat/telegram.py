from re import compile as re_compile
from requests import get, post, ConnectionError, exceptions, Timeout



class Telegram():
    def __init__(self, token='', client_id=''):
        self.api = 'https://api.telegram.org/bot'
        self._token = token
        self._client_id = str(client_id)

        p = re_compile(r"^\d{1,10}:[A-z0-9-_]{35,35}$")
        if not p.match(token):
            raise Exception('Telegram token is invalid')

        p = re_compile(r"^-?\d{7,13}$")
        if not p.match(client_id):
            raise Exception('Telegram client_id is invalid')

        #print('Telegram configure with for client "' + client_id + '" with token "' + token + '"')

    def send(self, message='') -> str:
        try:
            escaped_message = message.translate(message.maketrans({"*":  r"\*"}))
            payload = self.api + self._token + '/sendMessage?chat_id=' + self._client_id + '&parse_mode=Markdown&text=' + escaped_message
            resp = get(payload)

            if resp.status_code != 200:
                return ''

            resp.raise_for_status()
            json = resp.json()

        except ConnectionError as err:
            print(err)
            return ''

        except exceptions.HTTPError as err:
            print(err)
            return ''

        except Timeout as err:
            print(err)
            return ''

        return json

    def sendDoc(self, message='', doc='') -> str:
        try:
            escaped_message = message.translate(message.maketrans({"*":  r"\*"}))
            data = {"chat_id": self._client_id, "caption": escaped_message}
            url = self.api + self._token + '/sendPhoto'
            with open(doc, "rb") as image_file:
                resp = post(url, data=data, files={"photo": image_file})

            if resp.status_code != 200:
                return ''

            resp.raise_for_status()
            json = resp.json()

        except ConnectionError as err:
            print(err)
            return ''

        except exceptions.HTTPError as err:
            print(err)
            return ''

        except Timeout as err:
            print(err)
            return ''

        return json
