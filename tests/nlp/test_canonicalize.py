from nlp.canonicalize import canonicalize
def mk_app4():
    # mimic parser for "1 -> 0": ((( '1' '-' ) '>' ) '0')
    class V: 
        def __init__(self,n): self.name=n
    class A:
        def __init__(self,f,a): self.func=f; self.arg=a
    return A(A(A(V("1"), V("-")), V(">")), V("0"))

def test_split_arrow_canonicalizes():
    ast = mk_app4()
    can = canonicalize(ast)
    assert isinstance(can, tuple) and can[0] == "->" and can[1] in (1,"1") and can[2] in (0,"0")
