def trace_to_proof(trace, result):
    lines = []
    indent = "  "

    for i, step in enumerate(trace):
        phase = step.get("phase")
        prefix = f"{i+1}. "

        if phase == "APPLICATION":
            lines.append(f"{prefix}Apply {step['func']} to {step['arg']}")
        elif phase == "VARIABLE":
            val = step.get("value")
            lines.append(f"{prefix}Resolve variable {step['name']} → {val}")
        elif phase == "LAMBDA":
            lines.append(f"{prefix}Encountered λ{step['var']} -> {step['body']}")
        elif phase == "DEFINE":
            lines.append(f"{prefix}Define {step['name']} := {step['value']}")
        elif phase == "MEMORY":
            lines.append(f"{prefix}Lookup memory {step['var']} → {step['value']}")
        elif phase == "SUBSTITUTION":
            lines.append(f"{prefix}Substitute {step['var']} := {step['value']} in body")
        elif phase == "LITERAL":
            lines.append(f"{prefix}Literal value: {step['value']}")
        elif phase == "UNKNOWN":
            lines.append(f"{prefix}Unknown phase: {step['expr']}")
        else:
            lines.append(f"{prefix}Unhandled phase: {step}")

    lines.append("")
    lines.append(f"{'✅' if result == 'Alive' else '❌'} Final Result: {result}")
    return "\n".join(lines)
