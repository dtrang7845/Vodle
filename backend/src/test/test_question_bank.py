from app.data.question_bank import (
    QUESTION_BANK,
    question_bank_drafts,
    question_bank_size,
)


def test_question_bank_has_expected_size_and_shape():
    assert question_bank_size() == 300
    assert len(QUESTION_BANK) == 300

    drafts = question_bank_drafts()
    assert len(drafts) == 300
    assert all(len(draft.options) == 4 for draft in drafts)
