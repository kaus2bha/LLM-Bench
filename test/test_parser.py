from evaluation.response_parser import extract_final_answer


def test_extract_final_answer():
    assert extract_final_answer("Paris") == "Paris"