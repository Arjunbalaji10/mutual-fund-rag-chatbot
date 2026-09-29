import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from rag_pipeline import answer_question, load_resources


TEST_CASES = [
    {
        "question": "What is the expense ratio of HDFC Large Cap Fund Direct Growth?",
        "expected": "1.03%",
        "source": "hdfc-large-cap-fund-direct-growth",
    },
    {
        "question": "What is the minimum investment amount for HDFC Equity Fund Direct Growth?",
        "expected": "₹100",
        "source": "hdfc-equity-fund-direct-growth",
    },
    {
        "question": "What is the expense ratio of HDFC ELSS Tax Saver Fund Direct Plan Growth?",
        "expected": "1.21%",
        "source": "hdfc-elss-tax-saver-fund-direct-plan-growth",
    },
    {
        "question": "What is the minimum investment amount for HDFC Small Cap Fund Direct Growth?",
        "expected": "₹100",
        "source": "hdfc-small-cap-fund-direct-growth",
    },
    {
        "question": "What is the expense ratio of HDFC Balanced Advantage Fund Direct Growth?",
        "expected": "0.78%",
        "source": "hdfc-balanced-advantage-fund-direct-growth",
    },
    {
        "question": "What is the exit load of HDFC Large Cap Fund Direct Growth?",
        "expected": "1%",
        "source": "hdfc-large-cap-fund-direct-growth",
    },
    {
        "question": "Should I invest in HDFC Small Cap Fund to get higher returns?",
        "expected": "I can provide factual information",
        "source": None,
    },
    {
        "question": "What is the expense ratio of HDFC Flexi Cap Fund?",
        "expected": "I don't know based on the available sources.",
        "source": None,
    },
]


def main():
    print("Loading RAG resources...")
    chunks, retriever, groq_client = load_resources()

    passed = 0

    print("\nRunning evaluation...\n")

    for number, test in enumerate(TEST_CASES, start=1):
        result = answer_question(
            test["question"],
            chunks,
            retriever,
            groq_client,
        )

        answer = result["answer"]
        source_url = result["source_url"]

        normalized_answer = (
            answer.lower()
            .replace("\u202f", "")
            .replace(" ", "")
        )

        normalized_expected = (
            test["expected"].lower()
            .replace("\u202f", "")
            .replace(" ", "")
        )

        answer_pass = normalized_expected in normalized_answer

        source_pass = True

        if test["source"]:
            source_pass = (
                source_url is not None
                and test["source"] in source_url
            )
        else:
            source_pass = source_url is None

        test_pass = answer_pass and source_pass

        if test_pass:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(f"{number}. {status}")
        print(f"Question: {test['question']}")
        print(f"Answer: {answer}")
        print(f"Source: {source_url}")
        print("-" * 70)

    print(
        f"\nResult: {passed}/{len(TEST_CASES)} tests passed."
    )


if __name__ == "__main__":
    main()