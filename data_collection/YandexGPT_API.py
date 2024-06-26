import json
import logging
import requests
import configparser
from pprint import pprint


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s @ %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
logger = logging.getLogger(name="YaGPT-API")


class YandexGPTApi:
    def __init__(self, config: str) -> None:
        self._config = configparser.ConfigParser()
        self._config.read(config)

        self._api_key = self._config.get('Security', 'API-key')
        self._folder_id = self._config.get('Security', 'folder-id')
        self._request_url = self._config.get('YandexGPT', 'requests-url')
        self._model = self._config.get('YandexGPT', 'model')

    def _generate_promt(self,
                        message: list,
                        stream: bool = False,
                        temperature: float = 0.6,
                        max_tokens: int = 100) -> dict:
        prompt = {
            "modelUri": f"gpt://{self._folder_id}/{self._model}",
            "completionOptions": {
                "stream": stream,
                "temperature": temperature,
                "maxTokens": f"{max_tokens}"
            },
            "messages": message
        }
        return prompt

    def make_request(self,
                     user_message: list,
                     stream: bool = False,
                     temperature: float = 0.6,
                     max_tokens: int = 100
                     ) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self._api_key}"
        }

        try:
            response = requests.post(self._request_url,
                                     headers=headers,
                                     json=self._generate_promt(user_message,
                                                               stream=stream,
                                                               temperature=temperature,
                                                               max_tokens=max_tokens))
        except requests.RequestException as error:
            logger.error(error)
        else:
            return self._get_answer_text(response)
        return ""

    @staticmethod
    def _get_answer_text(answer) -> str:
        if answer:
            try:
                result = json.loads(answer.text)['id']
            except KeyError as error:
                logger.error(error)
            else:
                return result
        return ""
