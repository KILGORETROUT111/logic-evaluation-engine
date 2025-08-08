# src/nlp/scope_inference.py
# LEE v3.0 — Phase 6
# Free/Bound sets, capture checks, and a minimal scope graph for λ/quantifiers.

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from core.expressions import Variable, Lambda, Application, Quantifier, Expression
from nlp.rewriter import _fresh_name, alpha_rename  # reuse hygiene helpers

# ---------------------------
# Free / Bound variable sets
# ---------------------------

def free_vars(expr: Expression) -> Set[str]:
    """Standard free-variable set for our AST."""
    if isinstance(expr, Variable):
        return {expr.name}
    if isinstance(expr, Lambda):
        return free_vars(expr.body) - {expr.param.name}
    if isinstance(expr, Application):
        return free_vars(expr.func) | free_vars(expr.arg)
    if isinstance(expr, Quantifier):
        return free_vars(expr.body) - {expr.var.name}
    return set()

def bound_vars(expr: Expression) -> Set[str]:
    """All variables that are bound by some binder in expr."""
    if isinstance(expr, Variable):
        return set()
    if isinstance(expr, Lambda):
        return {expr.param.name} | bound_vars(expr.body)
    if isinstance(expr, Application):
        return bound_vars(expr.func) | bound_vars(expr.arg)
    if isinstance(expr, Quantifier):
        return {expr.var.name} | bound_vars(expr.body)
    return set()

# ---------------------------
# Scope Graph
# ---------------------------

@dataclass
class ScopeNode:
    """Represents a binder site and references bound by it."""
    binder: str                               # the variable name introduced here
    kind: str                                  # "lambda" or "forall"/"exists"
    parent: Optional[int] = None               # parent scope node id
    children: List[int] = field(default_factory=list)
    refs: List[int] = field(default_factory=list)  # indices into 'references' list

@dataclass
class Reference:
    """A variable reference with a resolution to some binder scope (or None if free)."""
    name: str
    resolved_scope: Optional[int]              # index into scope_nodes, or None if free

@dataclass
class ScopeGraph:
    nodes: List[ScopeNode] = field(default_factory=list)
    references: List[Reference] = field(default_factory=list)

    def add_node(self, node: ScopeNode) -> int:
        self.nodes.append(node)
        return len(self.nodes) - 1

    def add_reference(self, ref: Reference) -> int:
        self.references.append(ref)
        return len(self.references) - 1

def analyze_scopes(expr: Expression) -> ScopeGraph:
    """
    Build a scope graph: each λ/quantifier creates a new node.
    Variable references are resolved to the innermost matching binder (if any).
    """
    g = ScopeGraph()

    def walk(e: Expression, scope_stack: List[int]):
        if isinstance(e, Variable):
            # resolve to nearest matching binder
            resolved = None
            for sid in reversed(scope_stack):
                if g.nodes[sid].binder == e.name:
                    resolved = sid
                    break
            ridx = g.add_reference(Reference(name=e.name, resolved_scope=resolved))
            if resolved is not None:
                g.nodes[resolved].refs.append(ridx)
            return

        if isinstance(e, Lambda):
            node = ScopeNode(binder=e.param.name, kind="lambda", parent=scope_stack[-1] if scope_stack else None)
            nid = g.add_node(node)
            if scope_stack:
                g.nodes[scope_stack[-1]].children.append(nid)
            walk(e.body, scope_stack + [nid])
            return

        if isinstance(e, Quantifier):
            node = ScopeNode(binder=e.var.name, kind=e.kind, parent=scope_stack[-1] if scope_stack else None)
            nid = g.add_node(node)
            if scope_stack:
                g.nodes[scope_stack[-1]].children.append(nid)
            walk(e.body, scope_stack + [nid])
            return

        if isinstance(e, Application):
            walk(e.func, scope_stack)
            walk(e.arg, scope_stack)
            return

    walk(expr, [])
    return g

# ---------------------------
# Capture checks / hygiene
# ---------------------------

def would_capture(expr: Expression, binder: str, value: Expression) -> bool:
    """
    If substituting a variable x in a context where 'binder' is a lambda/quantifier binder,
    capture happens if binder ∈ free_vars(value) and the substitution would insert value under that binder.
    Use this helper to decide when you must alpha-rename the binder before substitution.
    """
    fvs = free_vars(value)
    return binder in fvs

def hygienic_rename_for_subst(body: Expression, binder: str, value: Expression) -> Tuple[Expression, str]:
    """
    If inserting 'value' under a binder would capture, alpha-rename the binder to a fresh symbol.
    Returns (new_body, new_binder_name).
    """
    if not would_capture(body, binder, value):
        return (body, binder)
    avoid = free_vars(body) | free_vars(value) | {binder}
    fresh = _fresh_name(binder, avoid)
    return (alpha_rename(body, binder, fresh), fresh)
