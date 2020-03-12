from app.common.extension import session

SHELL_CONTEXT = dict(
    session=session,
)


def inject_shell_context(**kwargs):
    for key, val in kwargs.items():
        globals()['SHELL_CONTEXT'][key] = val
