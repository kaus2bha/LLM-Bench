import os
import pandas as pd


def save_results(
    results,
    output_path="data/results/benchmark_results.csv"
):
    """
    Save benchmark results to CSV.
    """

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    rows = []

    for result in results:

        evaluation = result["evaluation"]

        rows.append({
            "question_id": result["question_id"],
            "model": result["model"],
            "evaluation_type": result["evaluation_type"],
            "category": result["category"],
            "difficulty": result["difficulty"],
            "final_answer": result["final_answer"],

            "evaluation_score": evaluation["score"],
            "evaluation_status": evaluation["status"],
            "evaluation_details": str(
                evaluation["details"]
            ),

            "response_status": result.get(
                "response_status",
                "unknown"
            ),
            "finish_reason": result.get(
                "finish_reason"
            ),

            "latency": result.get("latency"),
            "input_tokens": result.get("input_tokens"),
            "output_tokens": result.get("output_tokens"),

            "error": result.get("error")
        })

    df = pd.DataFrame(rows)

    df.to_csv(
        output_path,
        index=False
    )

    return df