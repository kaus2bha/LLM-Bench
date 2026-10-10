from abc import ABC, abstractmethod


class BaseModel(ABC):

    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate(self, prompt: str) -> dict:
        """
        Generate a response from the model.

        Returns:
            dict containing:
            - response
            - latency
            - token usage
        """
        pass