
from evaluation.evaluator import EvaluationEngine


def test_exact_evaluation():
    engine = EvaluationEngine()

    result = engine.evaluate(
        evaluation_type="exact",
        question_id="Q001",
        answer="Paris",
        ground_truth="Paris"
    )

    assert result["score"] == 1.0


def test_normalized_evaluation():
    engine = EvaluationEngine()

    result = engine.evaluate(
        evaluation_type="normalized",
        question_id="Q003",
        answer="180 km.",
        ground_truth="180 km"
    )

    assert result["score"] == 1.0


def test_rubric_evaluation():
    engine = EvaluationEngine()

    result = engine.evaluate(
        evaluation_type="rubric",
        question_id="Q007",
        answer="Clearly define the problem first.",
        ground_truth=""
    )

    assert result["score"] == 1.0



def test_unsupported_evaluation():
    engine = EvaluationEngine()

    result = engine.evaluate(
        evaluation_type="something_random",
        question_id="Q999",
        answer="test",
        ground_truth="test"
    )

    assert result["status"] == "unsupported_evaluation_type"

def test_hallucination_evaluation():
    engine = EvaluationEngine()

    result = engine.evaluate(
        evaluation_type="hallucination",
        question_id="Q008",
        answer="Zorvia is a fictional country, so it had no real president.",
        ground_truth=""
    )

    assert result is not None
    assert "score" in result


def test_ambiguity_evaluation():
    engine = EvaluationEngine()

    result = engine.evaluate(
        evaluation_type="ambiguity",
        question_id="Q009",
        answer="There is no single best programming language; it depends on the use case.",
        ground_truth=""
    )

    assert result is not None
    assert "score" in result
