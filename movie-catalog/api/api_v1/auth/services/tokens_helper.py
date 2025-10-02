import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    """
    Необходимо:
    - Проверка наличия токена
    - Генерация токена
    - Добавление токена в хранилище
    - Генерация токена и добавление в хранилище
    """

    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Проверка наличия токена.

        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Добавление токена в хранилище.

        :param token:
        :return:
        """

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Получение списка всех токенов из хранилища.

        :param:
        :return:
        """

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """
        Удаление токена из хранилища.

        :param token:
        :return:
        """
