import os
import time

from groq import Groq

from models.base_model import BaseModel


class GroqModel(BaseModel):

    def __init__(self, model_name: str):
        super().__init__(model_name)

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, prompt: str) -> dict:

        start_time = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens= 1024,
        )

        end_time = time.perf_counter()

        latency = end_time - start_time

        return {
            "model": self.model_name,
            "response": response.choices[0].message.content,
            "latency": latency,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "finish_reason": response.choices[0].finish_reason
        }