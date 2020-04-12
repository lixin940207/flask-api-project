# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/12
from app.app import create_app
import typing
import os
import click
from flask.cli import AppGroup
from app.common.extension import session


app = create_app(os.getenv('ENV', 'development'))
app_cli = AppGroup('app', help='some commands work with app.')


@app.shell_context_processor
def make_shell_context() -> typing.Dict:
    return dict(
        dict(
            session=session,
        ),
        app=app,
    )


@app_cli.command('print')
@click.argument('name')
def print_app_attr_by_name(name) -> None:
    """
    > flask app print config
    <Config {...}>
    """
    print(getattr(app, name, None))


app.cli.add_command(app_cli)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10001)

