# src/nlp/parser.py
# LEE v3.0 — Phase 6
# Symbolic parser → core AST (Variable, Lambda, Application, Quantifier)

from dataclasses import dataclass
from typing import List, Tuple, Optional
from core.expressions import Variable, Lambda, Application, Quantifier, Expression

# Supported surface forms:
#  - Variables:    x, x1, Patient, fever
#  - Lambda:       λx. expr    |  lambda x . expr
#  - Application:  (f a)       |  f a   (left-assoc; parenthesis recommended)
#  - Quantifiers:  forall x . expr   |  exists y . expr
#  - Parens:       ( ... )

_LAMBDA_SIGNS = {"λ", "lambda"}
_QUANT_KWS = {"forall": "forall", "exists": "exists"}

########################
# Lexer
########################
@dataclass
class Tok:
    kind: str
    text: str

def _is_ident_char(c: str) -> bool:
    return c.isalnum() or c == "_" or c == "-"

def lex(s: str) -> List[Tok]:
    s = s.strip()
    i, n = 0, len(s)
    out: List[Tok] = []
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1; continue
        if c in "()·.":
            out.append(Tok(c, c)); i += 1; continue
        if c in {"λ"}:
            out.append(Tok("LAMBDA", "λ")); i += 1; continue
        # words / identifiers
        if _is_ident_char(c):
            j = i
            while j < n and _is_ident_char(s[j]):
                j += 1
            word = s[i:j]
            if word in _QUANT_KWS:
                out.append(Tok("QUANT", word))
            elif word == "lambda":
                out.append(Tok("LAMBDA", "λ"))
            else:
                out.append(Tok("IDENT", word))
            i = j; continue
        # unknown single char token (treat as ident to be forgiving)
        out.append(Tok("IDENT", c)); i += 1
    return out

########################
# Parser (recursive descent)
########################
class Parser:
    def __init__(self, tokens: List[Tok]):
        self.toks = tokens
        self.i = 0

    def _peek(self, k: int = 0) -> Optional[Tok]:
        j = self.i + k
        return self.toks[j] if 0 <= j < len(self.toks) else None

    def _eat(self, kind: Optional[str] = None) -> Tok:
        t = self._peek()
        if t is None:
            raise ValueError("Unexpected end of input")
        if kind and t.kind != kind and t.text != kind:
            raise ValueError(f"Expected {kind}, got {t.kind}:{t.text}")
        self.i += 1
        return t

    def parse(self) -> Expression:
        expr = self._parse_expr()
        if self._peek() is not None:
            raise ValueError(f"Unexpected token {self._peek()}")
        return expr

    def _parse_expr(self) -> Expression:
        # Quantifier | Lambda | Application chain
        t = self._peek()
        if t and t.kind == "QUANT":
            return self._parse_quantifier()
        if t and t.kind == "LAMBDA":
            return self._parse_lambda()
        return self._parse_application_chain()

    def _parse_quantifier(self) -> Expression:
        kw = self._eat("QUANT").text  # forall/exists
        var_tok = self._eat("IDENT")
        var = Variable(var_tok.text)
        self._eat(".")
        body = self._parse_expr()
        return Quantifier(kind=_QUANT_KWS[kw], var=var, body=body)

    def _parse_lambda(self) -> Expression:
        self._eat("LAMBDA")
        param = self._eat("IDENT").text
        self._eat(".")
        body = self._parse_expr()
        return Lambda(Variable(param), body)

    def _parse_atom(self) -> Expression:
        t = self._peek()
        if t is None:
            raise ValueError("Unexpected end while reading atom")
        if t.text == "(":
            self._eat("(")
            inner = self._parse_expr()
            self._eat(")")
            return inner
        if t.kind == "IDENT":
            self._eat()
            return Variable(t.text)
        raise ValueError(f"Unexpected token in atom: {t}")

    def _parse_application_chain(self) -> Expression:
        # left-associative: a b c → ((a b) c)
        lhs = self._parse_atom()
        while True:
            t = self._peek()
            if t is None: break
            if t.text == ")" or t.text == ".":
                break
            # If next token starts a new atom, treat as application
            if t.kind in {"IDENT"} or t.text == "(" or t.kind in {"LAMBDA", "QUANT"}:
                rhs = self._parse_atom() if t.kind in {"IDENT"} or t.text == "(" else self._parse_expr()
                lhs = Application(lhs, rhs)
            else:
                break
        return lhs

def parse(text: str) -> Expression:
    return Parser(lex(text)).parse()
