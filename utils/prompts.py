def build_benchmark_prompt(question: str, context: str = "") -> str:

    if context:
        return f"""
You are being evaluated as part of an LLM benchmarking experiment.

Use the provided context to answer the question.

Context:
{context}

Question:
{question}

Provide a concise answer. Do not include unnecessary explanation.
""".strip()

    return f"""
You are being evaluated as part of an LLM benchmarking experiment.

Answer the question accurately and concisely.

Question:
{question}

Provide only the answer or a brief explanation when reasoning is necessary.
""".strip()