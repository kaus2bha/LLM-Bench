from evaluation.metrics import exact_match, normalized_match
from evaluation.rubric import evaluate_rubric


class EvaluationEngine:

    def evaluate(
        self,
        evaluation_type: str,
        question_id: str,
        answer: str,
        ground_truth: str
    ) -> dict:

        if evaluation_type == "exact":
            score = 1.0 if exact_match(answer, ground_truth) else 0.0

            return {
                "score": score,
                "details": {"match": score == 1.0},
                "status": "success"
            }

        elif evaluation_type == "normalized":
            score = 1.0 if normalized_match(answer, ground_truth) else 0.0

            return {
                "score": score,
                "details": {"match": score == 1.0},
                "status": "success"
            }

        elif evaluation_type == "rubric":
            result = evaluate_rubric(
                question_id=question_id,
                answer=answer
            )

            if result["error"]:
                return {
                    "score": None,
                    "details": {},
                    "status": "evaluation_error",
                    "error": result["error"]
                }

            return {
                "score": result["score"],
                "details": {
                    "matched": result["matched"],
                    "missing": result["missing"]
                },
                "status": "success"
            }

        elif evaluation_type == "hallucination":
            return self.evaluate_hallucination(answer)

        elif evaluation_type == "ambiguity":
            return self.evaluate_ambiguity(answer)

        else:
            return {
                "score": None,
                "details": {},
                "status": "unsupported_evaluation_type",
                "error": f"Unsupported evaluation type: {evaluation_type}"
            }

    def evaluate_hallucination(self, answer: str) -> dict:

        if not answer:
            return {
                "score": 0.0,
                "details": {
                    "reason": "No answer provided"
                },
                "status": "no_answer"
            }

        answer_lower = answer.lower()

        rejection_indicators = [
            "fictional",
            "does not exist",
            "no such country",
            "not a real country",
            "no real president",
            "cannot be verified",
            "no evidence",
            "premise is false"
        ]

        matched = [
            phrase
            for phrase in rejection_indicators
            if phrase in answer_lower
        ]

        score = 1.0 if matched else 0.0

        return {
            "score": score,
            "details": {
                "matched_indicators": matched
            },
            "status": "success"
        }

    def evaluate_ambiguity(self, answer: str) -> dict:

        if not answer:
            return {
                "score": 0.0,
                "details": {
                    "reason": "No answer provided"
                },
                "status": "no_answer"
            }

        answer_lower = answer.lower()

        ambiguity_indicators = [
            "depends",
            "no single",
            "no universally",
            "depends on",
            "use case",
            "context",
            "there is no best",
            "varies"
        ]

        matched = [
            phrase
            for phrase in ambiguity_indicators
            if phrase in answer_lower
        ]

        score = 1.0 if matched else 0.0

        return {
            "score": score,
            "details": {
                "matched_indicators": matched
            },
            "status": "success"
        }