from core.expressions import Variable, Lambda, Application, Literal, Substitution
from core.states import State


def evaluate_full(expr, env=None):
    if env is None:
        env = {}

    if isinstance(expr, Variable):
        print(f"[EVAL] Variable lookup: {expr.name} | Env: {env}")
        return env.get(expr.name, State.JAM), env

    elif isinstance(expr, Literal):
        print(f"[EVAL] Literal value: {expr.value}")
        return State.ALIVE, env

    elif isinstance(expr, Lambda):
        print(f"[EVAL] Lambda abstraction over: {expr.var}")
        return expr, env

    elif isinstance(expr, Application):
        print(f"[EVAL] Application: {expr.func} applied to {expr.arg}")

        func_val, env = evaluate_full(expr.func, env)
        arg_val, env = evaluate_full(expr.arg, env)

        if isinstance(func_val, Lambda):
            print(f"[EVAL] Applying lambda with var {func_val.var} to arg: {arg_val}")

            new_env = env.copy()

            if isinstance(expr.arg, Variable) and expr.arg.name in env:
                new_env = env.copy()
                new_env[func_val.var] = env[expr.arg.name]
            else:
                new_env[func_val.var] = arg_val

            return evaluate_full(func_val.body, new_env)

        elif isinstance(func_val, State):
            return func_val, env

        else:
            print(f"[EVAL] Failed application: func_val = {func_val}")
            return State.JAM, env

    else:
        print(f"[EVAL] Unknown expression type: {expr}")
        return State.JAM, env