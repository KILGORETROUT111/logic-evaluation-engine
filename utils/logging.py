
def log_event(event_type, expr=None, env=None):
    print(f"[{event_type}] Expression: {expr} | Env: {env}")
    return f"{event_type}: {expr}"
