# -*- coding: utf-8 -*-
import os
import sys
from pprint import pprint
import click
import emoji

#import sys
#if "C:\\hackathon\\2023\\odious-ado" not in sys.path:
#   sys.path.append("C:\\hackathon\\2023\\odious-ado")

from odious_ado.settings import BaseConfig
from odious_ado.plugins.ado import *


@click.group(name="ado", help="Azure DeveOps utilities")
@click.pass_context
def ado(ctx):
    ctx.ensure_object(dict)
    # cluster = session.create({})
    # engine = session.factory.create({})
    config = BaseConfig()
    ctx.obj["client"] = AdoClient()

    pass


@ado.command()
@click.pass_context
def info(ctx) -> None:
    """
    Get ADO client info.
    """
    # results = session.info()
    #
    # if results is None:
    #     click.secho("Unable to connect to database.")
    # else:
    #     click.secho(tabulate(results, headers="keys", tablefmt="psql"))

@ado.group("work-items")
@click.pass_context
def work_items(ctx):
    pass


@work_items.command("read-state")
@click.argument("item_id", type=click.STRING, required=True)
@click.pass_context
def read_state(ctx,*args, **kwargs):
    client = ctx.obj.get("client")

    if kwargs is None or len(kwargs) == 0:
        click.secho("Work Item ID is required for this function")
        sys.exit(1)
    for v in kwargs.values():
        try:
            v = int(v)
        except Exception:
            raise Exception("wtf pass me a int")

        if client is None:
            click.secho("Unable to get ado client.")
        else:
            click.echo(f"{v} : {get_ADO_state(v)}")


@ado.group("projects")
@click.pass_context
def projects(ctx):
    pass


@projects.command("ls")
@click.pass_context
def list_projects(ctx):
    client = ctx.obj.get("client")

    if client is None:
        click.secho("Unable to get ado client.")
    else:
        get_projects_response = client.get_core_client.get_projects()
        index = 0
        while get_projects_response is not None:
            for project in get_projects_response:
                pprint("[" + str(index) + "] " + project.name)
                index += 1

            if isinstance(get_projects_response, list):
                get_projects_response = None


@projects.command("get-items")
@click.pass_context
def get_items(ctx):
    # Gets states for items in ADO within the specified project in the .env
    OA_ADO_PROJECT_NAME: str = os.getenv("OA_ADO_PROJECT_NAME", "")
    client = ctx.obj.get("client")
    if client is None:
        click.secho("Unable to get ado client.")
    else:
        get_projects_response = client.get_core_client.get_projects()

        if get_projects_response is None:
            click.echo("Was unable to find any projects for you brah!", color=True)

        else:
            for i in client.get_work_item_client:


                click.echo(f"{emoji.emojize(':robot:')} -=-{i.id} -=- {i.url}")
            # else:
            #     if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
            #         # Get the next page of projects
            #         get_projects_response = client.get_core_client.get_projects(
            #             continuation_token=get_projects_response.continuation_token)
            #     else:
            #         # All projects have been retrieved

