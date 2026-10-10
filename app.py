from dotenv import load_dotenv

from models.model_registry import get_model
from benchmark.runner import BenchmarkRunner
from utils.results import save_results

load_dotenv()


MODEL_NAMES = [
    "GPT-OSS-20B",
    "Qwen-27B"
]


def main():

    # Create model instances
    models = {
        name: get_model(name)
        for name in MODEL_NAMES
    }

    # Create benchmark runner
    runner = BenchmarkRunner(models)

    # Load benchmark questions
    questions = runner.load_questions(
        "data/questions.csv"
    )

    print(
        f"Loaded {len(questions)} benchmark questions."
    )

    # Run benchmark
    results = runner.run(questions)
    save_results(results)

    print(
    "\nResults saved to "
    "data/results/benchmark_results.csv"
    )

    print("\n")
    print("=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)

    print(
        f"Total evaluations: {len(results)}"
    )

    # Display results
    for result in results:

        print("\n" + "-" * 70)

        print(
            f"Question: {result['question_id']}"
        )

        print(
            f"Model: {result['model']}"
        )

        print(
            f"Answer: {result['final_answer']}"
        )
        
        evaluation = result["evaluation"]

        print("Evaluation:")
        print(f"Score: {evaluation['score']}")
        print(f"Status: {evaluation['status']}")

        if evaluation["details"]:
            print(f"Details: {evaluation['details']}")

        if result["latency"] is not None:

            print(
                f"Latency: "
                f"{result['latency']:.3f}s"
            )

        print(
            f"Tokens: "
            f"{result['input_tokens']} in / "
            f"{result['output_tokens']} out"
        )


if __name__ == "__main__":
    main()