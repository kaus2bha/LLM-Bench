import pandas as pd

from evaluation.response_parser import extract_final_answer
from utils.prompts import build_benchmark_prompt
from utils.results import save_results
from evaluation.evaluator import EvaluationEngine


class BenchmarkRunner:

    def __init__(self, models: dict):
        self.models = models
        self.evaluator = EvaluationEngine()

    def load_questions(self, filepath: str) -> pd.DataFrame:
        return pd.read_csv(filepath)

    def build_prompt(self, question: pd.Series) -> str:

        context = question.get("context", "")

        if pd.isna(context):
            context = ""

        return build_benchmark_prompt(
            question=question["question"],
            context=str(context).strip()
        )

    def run(self, questions: pd.DataFrame) -> list:

        results = []

        total_questions = len(questions)
        total_models = len(self.models)

        completed = 0
        total = total_questions * total_models

        for _, question in questions.iterrows():

            question_id = question["id"]

            prompt = self.build_prompt(question)

            print(
                f"\n[{completed + 1}/{total}] "
                f"Question: {question_id}"
            )

            for model_name, model in self.models.items():

                print(f"  → Running {model_name}...")

                try:

                    result = model.generate(prompt)

                    final_answer = extract_final_answer(
                        result["response"]
                    )
                    finish_reason = result.get("finish_reason")

                    if finish_reason == "length":
                        response_status = "truncated"
                    elif not final_answer:
                        response_status = "no_answer"
                    else:
                        response_status = "success"
                    

                    evaluation = self.evaluator.evaluate(
                        evaluation_type=question["evaluation_type"],
                        question_id=question_id,
                        answer=final_answer,
                        ground_truth=question["ground_truth"]
                    )
                    if response_status != "success":
                        evaluation["status"] = response_status

                    benchmark_result = {
                        "question_id": question_id,
                        "question": question["question"],
                        "context": question["context"],
                        "category": question["category"],
                        "difficulty": question["difficulty"],
                        "ground_truth": question["ground_truth"],
                        "evaluation_type": question["evaluation_type"],
                        "model": model_name,
                        "raw_response": result["response"],
                        "final_answer": final_answer,
                        "latency": result["latency"],
                        "input_tokens": result["input_tokens"],
                        "output_tokens": result["output_tokens"],
                        "evaluation": evaluation,
                        "response_status": response_status,
                        "finish_reason": finish_reason,
                        "error": None
                    }

                    results.append(benchmark_result)
                    save_results(results)

                    completed += 1

                    print(
                        f"     ✓ Completed "
                        f"({completed}/{total})"
                    )

                except Exception as e:

                    print(
                        f"     ✗ Error: "
                        f"{type(e).__name__}: {e}"
                    )

                    error_result ={
                        "question_id": question_id,
                        "question": question["question"],
                        "context": question["context"],
                        "category": question["category"],
                        "difficulty": question["difficulty"],
                        "ground_truth": question["ground_truth"],
                        "evaluation_type": question["evaluation_type"],
                        "model": model_name,

                        "raw_response": None,
                        "final_answer": "",

                        "latency": None,
                        "input_tokens": None,
                        "output_tokens": None,

                        "finish_reason": None,
                        "response_status": "model_error",

                        "evaluation": {
                            "score": None,
                            "details": {},
                            "status": "model_error",
                            "error": str(e)
                        },
                        "error": str(e)
                    }
                    results.append(error_result)
        
                    save_results(results)
                    completed += 1
                
        save_results(results)
        return results