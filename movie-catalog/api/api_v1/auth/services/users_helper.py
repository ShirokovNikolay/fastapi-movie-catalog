from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    """
    Нужно от обертки:
    - Получить пароль пользователя по username
    - Совпадает ли пароль username с переданным
    """

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        По переданному юзернейму находит пароль.

        Если юзернейма не существует, то вернет None.

        :param username: - имя пользователя
        :return: пароль пользователя, если он существует
        """

    @classmethod
    def check_passwords_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Проверка паролей на совпадение.
        """
        return password1 == password2

    def validate_user_password(self, username: str, password: str) -> bool:
        """
        Проверка пароля на совпадение с переданным.

        :param username: - пользователь, чей пароль проверяем
        :param password: - переданный пароль
        :return: True, если пароли совпадают. Иначе False
        """
        db_password = self.get_user_password(username)
        if db_password is None:
            return False

        return self.check_passwords_match(
            password1=db_password,
            password2=password,
        )
