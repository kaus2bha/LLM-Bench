from models.groq_model import GroqModel


AVAILABLE_MODELS = {
    "GPT-OSS-20B": {
        "provider": "groq",
        "model_id": "openai/gpt-oss-20b"
    },
    "Qwen-27B": {
        "provider": "groq",
        "model_id": "qwen/qwen3.8-27b"
    }
}


def get_model(model_name: str):

    config = AVAILABLE_MODELS[model_name]

    if config["provider"] == "groq":
        return GroqModel(
            model_name=config["model_id"]
        )

    raise ValueError(
        f"Unsupported provider: {config['provider']}"
    )