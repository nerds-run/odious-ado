# -*- coding: utf-8 -*-
import os

import click
from dotenv import load_dotenv

from odious_ado import __version__

from odious_ado.settings import BaseConfig
from odious_ado.cli.ado import ado as ado_commands
from odious_ado.cli.gh import github as gh_commands
from odious_ado.plugins.gh import Github

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


@main.command('sync', help="Entrypoint for github actions integration")
@click.option(
    "-i",
    "--ado-id",
    help="ADO item id. int need to be passed via the cmd line",
    default=os.getcwd(),
    required=True,

)
@click.option(
    "-s",
    "--item-state",
    help="state of the thing",
    default=os.getcwd(),
    required=True,

)
@click.pass_context
def sync_boards(ctx, ado_id: int, item_state: str):
    from odious_ado.plugins import gh
    # the experctation is that we are getting passed a id + + state
    ctx.ensure_object(dict)

    settings = BaseConfig.get_settings()
    ctx.ensure_object(dict)
    ctx.obj['client']: Github = Github(settings.GITHUB_ACCESS_TOKEN)


    settings = BaseConfig.get_settings()
    gh_org, repo = settings.GITHUB_REPOSITORY.split('/')
    gh_issue_ids = gh.get_i_issue_ids(organization=gh_org, repository_name=repo)
    project_id = gh.list_projects(ctx.obj['client'])
    issues = gh.get_issues(ctx.obj['client'])
    from odious_ado.plugins.ado.state import set_ADO_state, get_ADO_state



    for dnd in gh_issue_ids:
        db_id, pvti = gh.add_issue_to_project(append_label=True, project_id=project_id, content_id=dnd)
        for i in issues:
            # 921938
            i.add_to_labels(pvti)
            i.add_to_labels("poop")


            new_ado_id = set_ADO_state(ado_id, item_state)
            i.add_to_labels(f"ADO-{new_ado_id}")


    # # ", "
    # # ", "
    # # get_ADO_state
    # # set_ADO_state
    # # ",
    #
    # if kwargs is None or len(kwargs) == 2:
    #     click.secho("Work Item ID and State is required")
    #
    #     sys.exit(1)
    #
    # v = kwargs[1]
    #
    # v = int(v)
    #
    # w = kwargs[2]
    #
    # click.echo(f"{v, w} : {set_ADO_state(v, w)}")
    #
    # # ctx.obj['client']: Github = Github(settings.GITHUB_ACCESS_TOKEN)


main.add_command(ado_commands, "ado")
main.add_command(gh_commands, "gh")
