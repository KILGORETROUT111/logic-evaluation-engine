def trace_to_proof(trace):
    print("\nTrace-to-Proof View:\n")
    for idx, event in enumerate(trace, 1):
        if isinstance(event, dict):
            phase = event.get("phase", "UNKNOWN")
            value = event.get("value", None)
        else:
            phase = getattr(event, "phase", "UNKNOWN")
            value = getattr(event, "value", None)

        line = f"{idx:>2}. [{phase}]"
        if value is not None:
            line += f" {value}"
        print(line)