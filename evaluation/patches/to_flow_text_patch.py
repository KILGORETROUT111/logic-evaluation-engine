def to_flow_text(manager):
    lines = []
    for branch_id, state in manager.branches.items():
        lines.append(f"=== BRANCH: {branch_id} | PHASE: {state.phase} ===")
        for entry in state.trace:
            if "→ Derived" in entry:
                parts = entry.split("→ Derived ")[1]
                expr, rest = parts, ""
                if " via " in parts:
                    expr, rest = parts.split(" via ", 1)
                arrow = "➤"
                label = f"{arrow} {expr.strip()}"
                if rest:
                    from_src, *rule = rest.split(" using ")
                    label += f" ← from {from_src.strip()}"
                    if rule:
                        label += f" [{rule[0].strip()}]"
                lines.append(label)
            elif "CONTRADICTION" in entry or "UNSAFE" in entry or "Forked" in entry:
                lines.append(entry.replace("↳", "⤷").strip())
        if not any("→ Derived" in t for t in state.trace):
            lines.append("(no derivations yet)")
        lines.append("")  # blank line between branches
    return "\n".join(lines)