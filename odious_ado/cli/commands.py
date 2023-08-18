# -*- coding: utf-8 -*-
import os

import click
from dotenv import load_dotenv

from odious_ado import __version__

from odious_ado.settings import BaseConfig
from odious_ado.cli.ado import ado as ado_commands
from odious_ado.cli.gh import github as gh_commands


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-p",
    "--path",
    help="path to working dir",
    default=os.getcwd(),
    required=False,
    type=click.Path(dir_okay=True, file_okay=False, resolve_path=True),
)
@click.pass_context
def main(ctx, path) -> None:
    dotenv_path: str = f"{path}/.env"

    # TODO: check if file exists
    load_dotenv(dotenv_path=dotenv_path)

    ctx.ensure_object(dict)
    ctx.obj["app_path"] = path


@main.command(help="Application version information")
@click.pass_context
def version(ctx):
    click.secho(__version__)


main.add_command(ado_commands, "ado")
main.add_command(gh_commands, "gh")


@main.command('sync', help="Entrypoint for github actions integration")
@click.pass_context
def sync_boards(ctx):

    settings = BaseConfig.get_settings()
    ctx.ensure_object(dict)
    # ctx.obj['client']: Github = Github(settings.GITHUB_ACCESS_TOKEN)





