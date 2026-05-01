from fastapi import HTTPException, status

from app.data.question_bank import QUESTION_BANK
from app.schemas.question import GeneratedQuestionDraft, QuestionOptionCreate


class QuestionGenerationService:
    def _filtered_bank(
        self,
        topic_hint: str | None = None,
        used_question_texts: set[str] | None = None,
    ) -> list[dict[str, object]]:
        used_question_texts = used_question_texts or set()
        normalized_hint = topic_hint.strip().casefold() if topic_hint else None

        filtered = []
        for entry in QUESTION_BANK:
            if entry["question_text"] in used_question_texts:
                continue

            if normalized_hint:
                haystack = " ".join(
                    [
                        str(entry["title"]),
                        str(entry["description"]),
                        str(entry["question_text"]),
                        " ".join(str(tag) for tag in entry["tags"]),
                    ]
                ).casefold()
                if normalized_hint not in haystack:
                    continue

            filtered.append(entry)

        return filtered

    def generate_question_draft(
        self,
        topic_hint: str | None = None,
        used_question_texts: set[str] | None = None,
    ) -> GeneratedQuestionDraft:
        matching_questions = self._filtered_bank(topic_hint, used_question_texts)
        if not matching_questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No local question-bank drafts matched that request.",
            )

        entry = matching_questions[0]
        return GeneratedQuestionDraft(
            title=str(entry["title"]),
            description=str(entry["description"]),
            question_text=str(entry["question_text"]),
            options=[
                QuestionOptionCreate(option_text=str(option_text))
                for option_text in entry["options"]
            ],
        )


question_generation_service = QuestionGenerationService()
