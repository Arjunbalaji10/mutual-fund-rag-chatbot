ADVICE_KEYWORDS = [
    "should i invest",
    "should i buy",
    "should i sell",
    "which fund should i choose",
    "best mutual fund",
    "best fund",
    "recommend",
    "recommendation",
    "where should i invest",
    "is this a good investment",
]


MUTUAL_FUND_KEYWORDS = [
    "mutual fund",
    "fund",
    "sip",
    "elss",
    "expense ratio",
    "exit load",
    "riskometer",
    "benchmark",
    "lock-in",
    "lock in",
    "tax",
    "statement",
    "scheme",
    "hdfc",
]


def check_guardrail(question):
    question_lower = question.lower().strip()

    # 1. Empty question
    if not question_lower:
        return {
            "allowed": False,
            "reason": "empty",
            "message": "Please enter a mutual fund question.",
        }

    # 2. Investment advice
    for keyword in ADVICE_KEYWORDS:
        if keyword in question_lower:
            return {
                "allowed": False,
                "reason": "advice",
                "message": (
                    "I can provide factual information about mutual funds, "
                    "but I cannot provide investment advice or recommendations."
                ),
            }

    # 3. Off-topic question
    if not any(
        keyword in question_lower
        for keyword in MUTUAL_FUND_KEYWORDS
    ):
        return {
            "allowed": False,
            "reason": "off_topic",
            "message": (
                "I can only answer factual questions about the mutual funds "
                "covered by my knowledge base."
            ),
        }

    # 4. Relevant question
    return {
        "allowed": True,
        "reason": "allowed",
        "message": "",
    }


if __name__ == "__main__":
    test_questions = [
        "What is the expense ratio?",
        "Should I invest in HDFC Large Cap Fund?",
        "What is the weather today?",
    ]

    for question in test_questions:
        result = check_guardrail(question)

        print(f"\nQuestion: {question}")
        print(f"Allowed: {result['allowed']}")
        print(f"Reason: {result['reason']}")
        print(f"Message: {result['message']}")