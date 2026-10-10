
import json
import pandas as pd

from evaluation.evaluator import EvaluationEngine


RESULTS_PATH = "data/results/benchmark_results.csv"
QUESTIONS_PATH = "data/questions.csv"
OUTPUT_PATH = "data/results/benchmark_results_reevaluated.csv"


def main():
    # Load existing benchmark results and original questions.
    results_df = pd.read_csv(RESULTS_PATH)
    questions_df = pd.read_csv(QUESTIONS_PATH)

    required_results = {
        "question_id",
        "model",
        "evaluation_type",
        "final_answer",
        "evaluation_score",
        "evaluation_status",
        "evaluation_details",
        "response_status",
    }
    missing = required_results - set(results_df.columns)

    if missing:
        raise ValueError(
            f"Results CSV is missing required columns: {sorted(missing)}"
        )

    # Get authoritative ground truth from the original question dataset.
    questions_df["id"] = questions_df["id"].astype(str).str.strip()
    ground_truth_map = questions_df.set_index("id")["ground_truth"].to_dict()

    results_df["question_id"] = (
        results_df["question_id"].astype(str).str.strip()
    )

    # Preserve old scores for comparison.
    results_df["old_evaluation_score"] = results_df["evaluation_score"]
    results_df["old_evaluation_status"] = results_df["evaluation_status"]

    engine = EvaluationEngine()
    reevaluated = 0
    skipped = 0

    for index, row in results_df.iterrows():
        question_id = row["question_id"]
        response_status = str(row["response_status"]).strip().lower()

        # Do not score failed, truncated, or empty model responses as normal.
        if response_status != "success":
            skipped += 1
            continue

        if question_id not in ground_truth_map:
            print(f"Skipping {question_id}: no matching question found.")
            skipped += 1
            continue

        answer = row["final_answer"]
        answer = "" if pd.isna(answer) else str(answer)

        ground_truth = ground_truth_map[question_id]
        ground_truth = (
            "" if pd.isna(ground_truth) else str(ground_truth)
        )

        evaluation = engine.evaluate(
            evaluation_type=str(row["evaluation_type"]),
            question_id=question_id,
            answer=answer,
            ground_truth=ground_truth,
        )

        results_df.at[index, "evaluation_score"] = evaluation["score"]
        results_df.at[index, "evaluation_status"] = evaluation["status"]
        results_df.at[index, "evaluation_details"] = json.dumps(
            evaluation.get("details", {}),
            ensure_ascii=False,
        )

        # Keep the existing error column if it exists.
        if "error" in results_df.columns:
            results_df.at[index, "error"] = evaluation.get("error")

        reevaluated += 1

    results_df.to_csv(OUTPUT_PATH, index=False)

    print("\nREEVALUATION COMPLETE")
    print(f"Rows loaded: {len(results_df)}")
    print(f"Rows reevaluated: {reevaluated}")
    print(f"Rows skipped: {skipped}")
    print(f"Saved to: {OUTPUT_PATH}")

    # Compare old and new average scores per model.
    results_df["old_evaluation_score"] = pd.to_numeric(
        results_df["old_evaluation_score"], errors="coerce"
    )
    results_df["evaluation_score"] = pd.to_numeric(
        results_df["evaluation_score"], errors="coerce"
    )

    successful = results_df[
        results_df["response_status"].astype(str).str.lower() == "success"
    ]

    comparison = successful.groupby("model").agg(
        old_average_score=("old_evaluation_score", "mean"),
        new_average_score=("evaluation_score", "mean"),
        evaluated_responses=("evaluation_score", "count"),
    )

    print("\nMODEL SCORE COMPARISON")
    print(comparison.round(3).to_string())


if __name__ == "__main__":
    main()
