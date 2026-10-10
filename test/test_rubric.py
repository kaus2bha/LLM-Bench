
from evaluation.rubric import check_criteria, evaluate_rubric


def test_rubric_matches_paraphrased_criterion():
    result = check_criteria(
        "Defining the problem clearly.",
        ["define the problem"]
    )

    assert result["score"] == 1.0
    assert result["matched"] == ["define the problem"]
    assert result["missing"] == []


def test_rubric_reports_missing_criteria():
    result = check_criteria(
        "Define the problem.",
        ["define the problem", "gather information"]
    )

    assert result["score"] == 0.5
    assert result["missing"] == ["gather information"]


def test_unknown_rubric_returns_error():
    result = evaluate_rubric("Q999", "Some answer")

    assert result["score"] is None
    assert result["error"] is not None
