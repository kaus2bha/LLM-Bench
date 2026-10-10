
from evaluation.metrics import exact_match, normalized_match


def test_exact_match():
    assert exact_match("Paris", "Paris")
    assert not exact_match("Paris.", "Paris")


def test_normalized_match():
    assert normalized_match("Paris.", "Paris")
    assert normalized_match(" PARIS ", "Paris")
    assert normalized_match("120 km", "120 km")


def test_normalized_match_with_units_and_explanations():
    assert normalized_match("100 °C", "100")
    assert normalized_match("60 cm²", "60 square centimeters")
    assert normalized_match("6", "6 days")
    assert normalized_match(
        "156 employees work outside engineering.", "156"
    )


def test_normalized_match_rejects_negated_answer():
    assert not normalized_match("not 100", "100")
