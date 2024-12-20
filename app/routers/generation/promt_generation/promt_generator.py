from abc import ABC, abstractmethod


class IPromptGenerator(ABC):

    @abstractmethod
    def generate_prompt(self, **kwargs) -> str:
        """ Метод для генерации промта """
