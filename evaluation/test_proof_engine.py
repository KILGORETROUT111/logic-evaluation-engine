from evaluation.proof_engine import ProofEngine

def test_proof_engine():
    engine = ProofEngine()

    # Axiom: ∀x.¬P(x) ∨ Q(x)
    engine.add_axiom("A1", "∀x.¬P(x) ∨ Q(x)")

    # Assume: P(a)
    engine.assume("P(a)")

    # Try to prove: Q(a)
    result, trace = engine.prove("Q(a)", given=["P(a)", "A1"])
    print("\nTest 1 — Q(a) from A1 + P(a):", result)
    for step in trace:
        print("  ", step)

    # Negative test: Prove something unrelated
    result2, trace2 = engine.prove("R(a)", given=["P(a)", "A1"])
    print("\nTest 2 — R(a) from A1 + P(a):", result2)
    for step in trace2:
        print("  ", step)

    # Direct assumption: R(b)
    engine.assume("R(b)")
    result3, trace3 = engine.prove("R(b)")
    print("\nTest 3 — R(b) from known fact:", result3)
    for step in trace3:
        print("  ", step)

if __name__ == "__main__":
    test_proof_engine()
