from core.expressions import Functor, Var, Value

def visualize_ast(expr):
    def recurse(node, counter=[0]):
        my_id = f"n{counter[0]}"
        counter[0] += 1
        if isinstance(node, Functor):
            label = node.name
            children = node.args
        elif isinstance(node, Var):
            label = node.name
            children = []
        elif isinstance(node, Value):
            label = str(node.val)
            children = []
        else:
            label = str(node)
            children = []

        result = [f'{my_id} [label="{label}"]']
        for child in children:
            cid, cres = recurse(child, counter)
            result.append(f"{my_id} -> {cid}")
            result.extend(cres)
        return my_id, result

    _, lines = recurse(expr)
    return "digraph G {
" + "
".join(lines) + "
}"