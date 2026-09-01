from backend.routing.router import IntentRouter


TEST_CASES = [
    ("Where is my order?", "order_support"),
    ("How long does standard shipping take?", "shipping"),
    ("Can I return this product?", "returns"),
    ("Where is my refund?", "refunds"),
    ("Can I cancel my order?", "cancellations"),
    ("My payment failed.", "payments"),
    ("I forgot my password.", "account_support"),
    ("Is this product compatible with my device?", "product_information"),
    ("What can you help me with?", "general_support"),
]


def main():
    router = IntentRouter()

    correct = 0

    print("=" * 70)
    print("ShopAssist AI - Intent Routing Evaluation")
    print("=" * 70)

    for message, expected in TEST_CASES:
        result = router.route(message)

        predicted = result["intent"]
        confidence = result["confidence"]

        is_correct = predicted == expected

        if is_correct:
            correct += 1

        status = "PASS" if is_correct else "FAIL"

        print(f"\n[{status}]")
        print(f"Message:    {message}")
        print(f"Expected:   {expected}")
        print(f"Predicted:  {predicted}")
        print(f"Confidence: {confidence:.2f}")

    accuracy = correct / len(TEST_CASES)

    print("\n" + "=" * 70)
    print(f"Correct: {correct}/{len(TEST_CASES)}")
    print(f"Accuracy: {accuracy:.2%}")
    print("=" * 70)


if __name__ == "__main__":
    main()
